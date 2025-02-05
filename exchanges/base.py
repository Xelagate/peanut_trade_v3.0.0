"""
Модуль base.py
--------------

Цей модуль містить базовий клас Exchange, який задає інтерфейс для роботи з криптобіржами.
Всі конкретні реалізації бірж (як централізованих, так і децентралізованих) повинні наслідуватися від цього класу
та реалізовувати метод get_latest_price для отримання останньої ціни за заданою парою валют.
"""

class Exchange:
    def __init__(self, name: str):
        """
        Ініціалізує екземпляр класу Exchange.

        Параметри:
            name (str): Назва біржі (наприклад, "binance", "kucoin" тощо).
        """
        self.name = name

    async def get_latest_price(self, base: str, quote: str) -> float:
        """
        Асинхронний метод, який має повернути останню (latest) ціну для пари base/quote.

        Параметри:
            base (str): Базова валюта (наприклад, "BTC").
            quote (str): Валюта котирування (наприклад, "USDT").

        Повертає:
            float: Остання ціна для заданої пари валют.

        Примітка:
            Цей метод не реалізовано в базовому класі, тому він повинен бути перевизначений
            у класах-нащадках, які представляють конкретні біржі.
        """
        raise NotImplementedError("Метод get_latest_price не реалізовано")
