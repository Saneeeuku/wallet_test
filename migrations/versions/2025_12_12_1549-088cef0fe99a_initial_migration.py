"""initial migration

Revision ID: 088cef0fe99a
Revises:
Create Date: 2025-12-12 15:49:27.292318

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from migrations.seed_data import seed_initial_data, clear_initial_data


revision: str = "088cef0fe99a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "wallets",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("balance", sa.Integer(), nullable=False),
        sa.CheckConstraint("balance >= 0", name="balance_non_negative"),
        sa.PrimaryKeyConstraint("id"),
    )

    connection = op.get_bind()
    seed_initial_data(connection)


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()
    clear_initial_data(connection)

    op.drop_table("wallets")
