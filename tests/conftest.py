from typing import AsyncIterable, AsyncGenerator

from pytest import fixture
from httpx import AsyncClient, ASGITransport

from db.db_base import null_pool_session
from main import app
from utils import DBManager, get_db


async def get_db_null_pool() -> AsyncIterable:
    async with DBManager(session_factory=null_pool_session) as db:
        yield db


@fixture(scope="session", autouse=True)
async def db() -> None:
    app.dependency_overrides[get_db] = get_db_null_pool


@fixture(scope="session", autouse=True)
async def ac(db) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@fixture(scope="function")
async def get_wallet_uuid(ac):
    response = await ac.get("/api/v1/wallets/")
    return response.json()["wallet"]
