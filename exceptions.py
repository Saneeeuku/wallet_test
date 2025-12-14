class BaseWalletException(Exception):
    detail: str = "Неустановленная ошибка"

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super().__init__(self.detail, *args, **kwargs)


class NonNegativeBalanceConstraintException(BaseWalletException):
    detail = "Баланс не может быть отрицательным"
