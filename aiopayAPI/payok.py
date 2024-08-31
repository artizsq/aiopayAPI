import aiohttp

from .config import PayConfig
from .urls import URL
from .types import Method
import json
from .exceptions import ResponseError
from .utils import Checker
from typing import Dict, Union
from .types.commissions import Commission
from pydantic import BaseModel





class PayOk:
    """
    Класс для работы с сайтом PayOk
    
    :param config: Конфиг для класса PayOk
    :type config: :obj:`PayConfig`, обязательно
    """
    def __init__(self, config: PayConfig):
        """
        Инициализация класса PayOk
        
        :param config: Конфиг для класса PayOk
        :type config: :obj:`PayConfig`, обязательно
        """
        self.api_id: int = config.API_ID
        """ID вашего ключа API"""

        self.key: str = config.API_KEY
        """Ваш ключ API"""

        self.shop: int = config.shop
        """ID магазина"""

        self.json: Union[str, None] = config.json_file
        """JSON файл для записи ответов"""

        self.error: bool = config.error
        """Обработка ошибок (boolean, default=False)"""

        

    async def payment(self, amount: float, method: Union[Method, str],
                      reciever: str, sbp_bank: Union[str, None] = None,
                      commission_type: Union[str, None] = None, url: Union[str, None] = None) -> Dict:
        """
        Создание выплат (перевод)\n
        
        
        :param amount: Сумма выплаты
        :type amount: :obj:`float`, обязательно

        :param method: Специальное значение метода выплаты 
        :type method: :obj:`Method, str`, обязательно

        :param reciever: Реквизиты получателя выплаты
        :type reciever: :obj:`str`, обязательно

        :param sbp_bank: Банк для выплаты по СБП
        :type sbp_bank: :obj:`str`, опционально

        :param commission_type: Тип расчета комиссии (Commission.balance | Commission.payment)
        :type commission_type: :obj:`str`, опционально

        :param url: URL для отправки Webhook при смене статуса выплаты
        :type url: :obj:`str`, опционально


        :return: :obj:`dict` с данными 
        """

        data = {
            "API_ID": self.api_id,
            "API_KEY": self.key,
            "amount": amount,
            "method": method,
            "reciever": reciever
        }
        data.update({"sbp_bank": sbp_bank}) if sbp_bank else None
        data.update({"comission_type": commission_type}) if commission_type else None
        data.update({"webhook_url": url}) if url else None

        async with aiohttp.ClientSession() as session:
            async with session.post(URL.create, data=data) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if self.json:
                        with open(self.json, "a", encoding='utf-8') as file:
                            json.dump(json.loads(text), file, 
                                    indent=4, ensure_ascii=False)
                    if self.error:
                        Checker().status(json.loads(text))
                    return json.loads(text)
                else:
                    raise ResponseError(resp.status)
                
    async def balance(self) -> Dict:
        """
        Получение баланса

        
        :return: :obj:`dict` с данными баланса
        """
        data = {
            "API_ID": self.api_id,
            "API_KEY": self.key,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(URL.balance, data=data) as resp:
                if resp.status != 200:
                    raise ResponseError(resp.status)
                
                text = await resp.text(encoding="utf-8")
                json_resp = json.loads(text)

                if self.json:
                    with open(self.json, 'a', encoding='utf-8') as file:
                        json.dump(json_resp, file, indent=4, ensure_ascii=False)
                if self.error:
                    Checker().status(json_resp)
                return json_resp
            

    async def payouts(self, offset: int = 0, payout_id: Union[int, None] = None) -> Dict:
        """
        Получение выплат (макс. 100)

        :param offset: Отступ, пропуск указанного количества строк
        :type offset: :obj:`int`, опционально

        :param payout_id: ID выплаты в системе Payok
        :type payout_id: :obj:`int`, опционально

        :return: :obj:`dict` объект с данными выплат
        """
        data = {
        "API_ID": self.api_id,
        "API_KEY": self.key
        }
        if payout_id:
            data["payout_id"] = payout_id
        if offset:
            data["offset"] = offset

        async with aiohttp.ClientSession() as session:
            async with session.post(URL.payout, data=data) as resp:
                if resp.status == 200:
                    text = await resp.text()

                    if self.json:
                        with open(self.json, 'a', encoding='utf-8') as file:
                            json.dump(json.loads(text), file, 
                                    indent=4, ensure_ascii=False)
                    if self.error:
                        Checker().status(json.loads(text))
                    return json.loads(text)
                else:
                    raise ResponseError(resp.status)







    





