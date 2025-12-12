from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class OperationType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

    @classmethod
    def _missing_(cls, input_value):
        if isinstance(input_value, str):
            normalized = input_value.strip().lower()

            for member in (cls.DEPOSIT, cls.WITHDRAW):
                if member.value == normalized:
                    return member

            raise ValueError(f"{input_value} не валидно {cls.__name__}")


class WalletOperationRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Сумма операции")
    operation_type: OperationType

    model_config = ConfigDict(from_attributes=True)


class WalletBalance(BaseModel):
    balance: int

    model_config = ConfigDict(from_attributes=True)


class Wallet(WalletBalance):
    id: int
