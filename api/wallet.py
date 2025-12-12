from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends

from schemas.wallet import WalletOperationRequest, WalletBalance
from utils import get_wallet_uuid, DBDep

router = r = APIRouter(prefix="/api/v1/wallets")


@r.post("/{wallet_uuid}/operation")
async def change_balance(
    wallet_uuid: Annotated[UUID, Depends(get_wallet_uuid)],
    operation_request: WalletOperationRequest,
    db: DBDep,
):
    result = await db.wallets.perform_operation(wallet_uuid,operation_request)
    return {"status": "OK", "balance": f"Новый баланс - {result.balance}"}
