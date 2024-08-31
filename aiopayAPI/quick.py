import hashlib
from typing import Dict, Optional
import json

from .config import QuickConfig
from .urls import URL
import aiohttp
from .utils import Checker
from .types import Method



class QuickPay:
    """Класс для создание оплаты в PayOk
    :param amount: Сумма оплаты
    :type amount: :obj:`float`
    :param payment: ID платежа в вашей системе
    :type payment: :obj:`str`, опционально
    :param shop: ID магазина
    :type shop: :obj:`int`
    :param desc: Описание платежа
    :type desc: :obj:`str`
    :param currency: Валюта платежа
    :type currency: :obj:`str`
    :param secret: Секретный ключ
    :type secret: :obj:`str`
    :param email: E-mail получателя
    :type email: :obj:`str`, опционально
    :param success_url: URL для отправки Webhook при смене статуса выплаты
    :type success_url: :obj:`str`, опционально
    :param method: Специальное значение метода выплаты, (default=Method.card)
    :type method: :obj:`Method`, опционально
    :param lang: Язык выплаты
    :type lang: :obj:`str`, опционально
    :param custom: Ваш параметр, который вы хотите передать в уведомлении
    :type custom: :obj:`str`, опционально
    :param API_ID: ID ключа (нужен ТОЛЬКО для получения транзакций)
    :type API_ID: :obj:`int`, опционально
    :param API_KEY: API Ключ (нужен ТОЛЬКО для получения транзакции)
    :type API_KEY: :obj:`str`, опционально
    :param json_file: JSON файл для записи ответов
    :type json_file: :obj:`str`, опционально
    :param processing_error: Обработка ошибок (boolean, default=False)
    :type processing_error: :obj:`bool`, опционально
    """
    def __init__(self, config: QuickConfig) -> None:
        """
        Инициализация класса Quickpay

        :param config: Конфиг для класса Quickpay
        :type config: :obj:`QuickConfig`
        """

        self.amount: float = config.amount
        """Сумма оплаты"""

        self.payment: int = config.payment
        """ID платежа в вашей системе"""

        self.shop: int = config.shop
        """ID магазина"""

        self.desc: str = config.desc
        """Описание платежа"""

        self.currency: str = config.currency
        """Валюта платежа (RUB, USD, EUR и тд)"""

        self.secret: str = config.secret
        """Секретный ключ"""

        self.json_file: str | None = config.json_file
        """JSON файл для записи ответов"""

        self.error: bool | None = config.error
        """Обработка ошибок (boolean, default=False)"""
        
       


    def generate_paylink(self, method: Optional[Method] = None, email: Optional[str] = None, 
                         success_url: Optional[str] = None, lang: Optional[str] = None, custom: Optional[str] = None) -> str:
        """
        Генерация ссылки для оплаты (функция)

        :param method: Специальное значение метода выплаты, (default=Method.card)
        :type method: :obj:`Method`, опционально

        :param email: E-mail получателя
        :type email: :obj:`str`, опционально

        :param success_url: URL для отправки Webhook при смене статуса выплаты
        :type success_url: :obj:`str`, опционально

        :param lang: Язык выплаты
        :type lang: :obj:`str`, опционально

        :param custom: Ваш параметр, который вы хотите передать в уведомлении
        :type custom: :obj:`str`, опционально
        
        :return: Ссылка
        """

        url = f"https://payok.io/pay?currency={self.currency}&amount={self.amount}&payment={self.payment}&desc={self.desc}&shop={self.shop}"
        if method:
            url += f"&method={method}"
        else:
            url += f"&method=cd"

        if email:
            url += "&email=" + email

        if success_url:
            url += f"&success_url={success_url}"

        if lang:
            url += f"&lang={lang}"

        if custom:
            url += f"&custom={custom}"


        secret = hashlib.md5(f"{self.amount}|{self.payment}|{self.shop}|{self.currency}|{self.desc}|{self.secret}".encode('utf-8')).hexdigest()
        url += f"&sign={secret}"

        return url

    async def get_transaction(self, API_ID: int, API_KEY: str) -> Dict:
        """
        Получение всех транзакций (макс. 100)

        :param API_ID: ID ключа 
        :type API_ID: :obj:`int`, обязательно

        :param API_KEY: API Ключ 
        :type API_KEY: :obj:`str`, обязательно

        :return: :obj:`dict` с данными транзакции
        """
        data = {
            "API_ID": API_ID,
            "API_KEY": API_KEY,
            "shop": self.shop
        }
        if self.payment:
            data.update({"payment": self.payment})

        async with aiohttp.ClientSession() as session:
            async with session.post(URL.transaction, 
                                    data=data) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if self.json_file:
                        with open(self.json_file, 'a', encoding='utf-8') as file:
                                json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
                    if self.error is True:
                        Checker().status(json.loads(text))
                    return json.loads(text)
                else:
                    return {}


