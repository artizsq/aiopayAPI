from typing import Union
from pydantic import BaseModel

from .types.methods import Method

from .types.commissions import Commission

class PayConfig(BaseModel):
    """
    Конфиг для класса PayOk

    :param API_ID: ID ключа
    :type API_ID: :obj:`int`

    :param API_KEY: API Ключ
    :type API_KEY: :obj:`str`

    :param shop: ID магазина
    :type shop: :obj:`int`

    :param json_file: JSON файл для записи ответов
    :type json_file: :obj:`str`, опционально

    :param error: Обработка ошибок (boolean, default=False)
    :type error: :obj:`bool`, опционально

    """
    API_ID: int
    """ID ключа"""

    API_KEY: str
    """API Ключ"""

    shop: int
    """ID магазина"""

    json_file: Union[str, None] = None
    """JSON файл для записи ответов"""

    error: bool = False
    """Обработка ошибок (boolean, default=False)"""


    
    
    
class QuickConfig(BaseModel):
    """
    Конфиг для класса QuickPay
    """
    amount: float 
    """Сумма оплаты"""

    shop: int
    """ID магазина"""

    desc: str
    """Описание платежа"""

    currency: str
    """Валюта платежа (RUB, USD, EUR и тд)"""

    secret: str
    """Секретный ключ"""

    payment: int
    """ID платежа в вашей системе (нужен для проверки оплаты)"""

    json_file: Union[str, None] = None
    """JSON файл для записи ответов запросов"""

    error: bool = False
    """Обработка ошибок (boolean, default=False)"""                 
