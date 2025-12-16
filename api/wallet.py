from uuid import UUID
from typing import Annotated

from sqlalchemy.exc import NoResultFound
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND

from fastapi import APIRouter, Depends, HTTPException

from exceptions import NonNegativeBalanceConstraintException
from schemas.wallet import WalletOperationRequest, WalletBalance, Wallet
from utils import get_wallet_uuid, DBDep

router = r = APIRouter(prefix="/api/v1/wallets")


@r.get("/", description="Получить id рандомного кошелька для дальнейшей работы")
async def get_wallet(
    wallet_uuid: Annotated[UUID, Depends(get_wallet_uuid)],
):
    return {"wallet": wallet_uuid}


@r.post("/{wallet_uuid}/operation", description="Изменить баланс, deposit или withdraw")
async def change_balance(db: DBDep, wallet_uuid: UUID, operation_request: WalletOperationRequest):
    try:
        result = await db.wallets.perform_operation(wallet_uuid, operation_request)
    except NonNegativeBalanceConstraintException as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=e.detail)
    except NoResultFound as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.args)
    return {"balance": f"Новый баланс - {result.balance}"}


@r.post("/{wallet_uuid}", description="Показать текущий баланс", response_model=WalletBalance)
async def get_balance(wallet_uuid: UUID, db: DBDep):
    try:
        result: Wallet = await db.wallets.get_one(id=wallet_uuid)
    except NoResultFound as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.args)
    return result
