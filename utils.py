from typing import Annotated
from uuid import UUID
from random import choice

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_base import session
from repositories.wallet import WalletRepository
from schemas.wallet import Wallet


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()

        self.wallets = WalletRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()


async def get_db():
    async with DBManager(session_factory=session) as db:
        yield db


async def get_wallet_uuid(db: DBManager = Depends(get_db)) -> UUID:
    uuids_from_db: list[Wallet] = await db.wallets.get_all()
    return choice(uuids_from_db).id

DBDep = Annotated[DBManager, Depends(get_db)]
