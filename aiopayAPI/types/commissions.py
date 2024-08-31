from enum import Enum
class Commission(Enum):
    """Комиссия платежа"""

    balance: str  = "balance"
    """Комисия с баланса"""

    payment: str = "payment"
    """Комиссия с платежа"""