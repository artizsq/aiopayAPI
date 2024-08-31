===============
Примеры
===============

На этой странице есть коды использования **aiopayAPI**

В скором времени сделаю примеры на GitHub

Получение баланса
-------------
.. code:: python
    from aiopayAPI.config import PayConfig
    from aiopayAPI import PayOk
    import asyncio

    payconfig = PayConfig(
        API_ID=1111, # Ваш ID от API
        API_KEY="some-api_key", # Ваш API ключ
        shop=4444 # ID от магазина
    )

    async def main():
        pay = PayOk(
            config=payconfig # Указываем наш PayConfig
        )
        balance = await pay.balance()
        print(balance)

    if __name__ == "__main__":
        asyncio.run(main())



Генерация ссылки
------------------
.. code:: python

    from aiopayAPI.config import QuickConfig
    from aiopayAPI import QuickPay
    import asyncio

    quickconfig = QuickConfig(
        amount=100.0,
        shop=44444,
        desc="test",
        currency="RUB",
        secret="секретный ключ магазина",
        payment=1 # ID платежа в вашей система (нужен для проверки оплаты)
    )

    async def main():
        quick = QuickPay(
            config=quickconfig
        )
        trans = quick.generate_paylink()
        print(trans)


Создание оплаты
-----------
.. code:: python
    from aiopayAPI.config import PayConfig
    from aiopayAPI import PayOk, Method
    import asyncio

    payconfig = PayConfig(
        API_ID=1111, # Ваш ID от API
        API_KEY="some-api_key", # Ваш API ключ
        shop=4444 # ID от магазина
    )

    async def main():
        pay = PayOk(
            config=payconfig
            
        )
        payout = await pay.payment(
            amount=100.0,
            reciever="4220 1154 4456 5263"
        )
        print(payout)

    if __name__ == "__main__":
        asyncio.run(main())


Получение оплаты
-------------
.. code:: python
    from aiopayAPI.config import PayConfig
    from aiopayAPI import PayOk, Method
    import asyncio

    payconfig = PayConfig(
        API_ID=1111, # ID вашего ключа
        API_KEY="xxxxxxxxxxxxxxxxxx", # Сам ключ
        shop=4444 # ID магазина
    )

    async def main():
        pay = PayOk(
            config=payconfig
        )
        payouts = await pay.payouts()
        print(payouts)

    if __name__ == "__main__":
        asyncio.run(main())

Получение транзакций
--------------
.. code:: python
    from aiopayAPI.config import QuickConfig
    from aiopayAPI import QuickPay, Method
    import asyncio

    quickconfig = QuickConfig(
        amount=100.0, # Можно ввести любые данные
        shop=44444, # Обязательно
        desc="test", # Можно ввести любые данные
        currency="RUB", # Можно ввести любые данные
        secret="секретный ключ магазина", # Можно ввести любые данные
        payment=1 # Обязательный параметр для проверки транзакции
    )

    async def main():
        quick = QuickPay(
            config=quickconfig
        )
        trans = await quick.get_transaction(
            API_KEY="xxxxxxxxx",
            API_ID=4444
        )
        print(trans)

    if __name__ == "__main__":
        asyncio.run(main())



Если вам не понятны данные примеры, вы можете посмотреть более подробные примеры на GitHub или на сайте Payok (https://payok.io/cabinet/documentation/doc_main.php)

