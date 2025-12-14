from pytest import mark
from httpx import AsyncClient, ASGITransport
from main import app


@mark.asyncio
async def test_all_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        response = await client.get("/api/v1/wallets/")
        assert response.status_code == 200
        wallet_uuid = response.json()["wallet"]

        response = await client.post(f"/api/v1/wallets/{wallet_uuid}")
        assert response.status_code in [200, 404]

        payloads = [
            {"operation_type": "deposit", "amount": 50},
            {"operation_type": "withdraw", "amount": 50},
        ]
        for p in payloads:
            response = await client.post(
                f"/api/v1/wallets/{wallet_uuid}/operation",
                json=p
            )
            assert response.status_code in [200, 404, 409]
