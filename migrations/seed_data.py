import uuid

from sqlalchemy import table, column, Integer, Uuid


def seed_initial_data(connection):
    wallets_table = table(
        "wallets",
        column("id", Uuid),
        column("balance", Integer),
    )

    wallets_data = [
        {
            "id": uuid.uuid4(),
            "balance": 0,
        },
        {
            "id": uuid.uuid4(),
            "balance": 100,
        },
        {
            "id": uuid.uuid4(),
            "balance": 1000,
        },
    ]

    connection.execute(wallets_table.insert(), wallets_data)


def clear_initial_data(connection):
    wallets_table = table("wallets")

    connection.execute(wallets_table.delete())
