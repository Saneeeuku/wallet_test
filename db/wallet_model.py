from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid, Integer

from db.db_base import Base


class WalletModel(Base):
    __tablename__ = "wallets"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    balance: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (CheckConstraint("balance >= 0", name="balance_non_negative"),)
