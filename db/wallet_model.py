import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid, Integer

from db.db_base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    balance: Mapped[int] = mapped_column(Integer)


