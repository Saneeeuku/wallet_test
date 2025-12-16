from pytest import mark, fixture


async def test_get_wallet_uuid(ac):
    response = await ac.get("/api/v1/wallets/")
    assert response.status_code == 200


@mark.parametrize(
    "wallet_uuid,get_wallet_uuid,status_code",
    [
        ("11111111-1111-1111-8223-b3a6624c0ede", "indirect", 404),
        (None, "indirect", 200),
    ],
    indirect=["get_wallet_uuid"],
)
async def test_get_balance(ac, wallet_uuid, status_code, get_wallet_uuid):
    if wallet_uuid is None:
        wallet_uuid = get_wallet_uuid

    response = await ac.post(f"/api/v1/wallets/{wallet_uuid}")
    assert response.status_code == status_code


@mark.parametrize(
    "wallet_uuid,get_wallet_uuid,status_code",
    [
        ("11111111-1111-1111-8223-b3a6624c0ede", "indirect", 404),
        (None, "indirect", 200),
    ],
    indirect=["get_wallet_uuid"],
)
async def test_operations(ac, wallet_uuid, status_code, get_wallet_uuid):
    payloads = [
        {"operation_type": "deposit", "amount": 50},
        {"operation_type": "withdraw", "amount": 50},
    ]

    if wallet_uuid is None:
        wallet_uuid = get_wallet_uuid

    for p in payloads:
        response = await ac.post(
            f"/api/v1/wallets/{wallet_uuid}/operation",
            json=p
        )
        assert response.status_code == status_code
