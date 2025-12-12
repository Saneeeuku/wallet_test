from uuid import UUID

from repositories.base import BaseRepository
from db.wallet_model import WalletModel
from schemas.wallet import Wallet, WalletOperationRequest, WalletBalance
from schemas.wallet import OperationType


class WalletRepository(BaseRepository):
    model = WalletModel
    schema = Wallet

    async def perform_operation(
        self,
        wallet_uuid: UUID,
        operation: WalletOperationRequest
    ) -> Wallet:
        if operation.operation_type == OperationType.WITHDRAW:
            operation.amount *= -1
        wallet: Wallet = await self.get_one(id=wallet_uuid)
        wallet.balance += operation.amount
        result: Wallet = await self.edit(wallet, id=wallet_uuid)
        return result
