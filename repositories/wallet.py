from uuid import UUID

from asyncpg import CheckViolationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from exceptions import NonNegativeBalanceConstraintException
from repositories.base import BaseRepository
from db.wallet_model import WalletModel
from schemas.wallet import Wallet, WalletOperationRequest
from schemas.wallet import OperationType


class WalletRepository(BaseRepository):
    model = WalletModel
    schema = Wallet

    async def perform_operation(
        self, wallet_uuid: UUID, operation: WalletOperationRequest
    ) -> Wallet:
        if operation.operation_type == OperationType.WITHDRAW:
            operation.amount *= -1

        query = select(self.model).filter_by(id=wallet_uuid).with_for_update()
        data_from_db = await self.session.execute(query)

        wallet: Wallet = self.schema.model_validate(data_from_db.scalar_one(), from_attributes=True)
        wallet.balance += operation.amount

        try:
            result: Wallet = await self.edit(wallet, id=wallet_uuid)
        except IntegrityError as e:
            if {isinstance(e.orig.__cause__, CheckViolationError)}:
                raise NonNegativeBalanceConstraintException from e

        await self.session.commit()

        return result
