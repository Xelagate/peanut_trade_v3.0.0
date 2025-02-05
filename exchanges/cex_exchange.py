"""
Модуль cex_exchange.py
-----------------------

Цей модуль містить клас CexExchange, який є базовим для централізованих бірж (CEX), що використовують бібліотеку ccxt.
Клас наслідується від базового класу Exchange і реалізує метод get_latest_price для отримання останньої ціни заданої пари валют.
"""

import ccxt
from .base import Exchange

class CexExchange(Exchange):
    def __init__(self, name: str, client):
        """
        Ініціалізує об'єкт CexExchange.

        Параметри:
            name (str): Назва біржі (наприклад, "binance", "kucoin" тощо).
            client: Екземпляр ccxt-клієнта, який використовується для взаємодії з API біржі
                    (наприклад, ccxt.binance() або ccxt.kucoin()).
        """
        super().__init__(name)
        self.client = client

    async def get_latest_price(self, base: str, quote: str) -> float:
        """
        Асинхронний метод для отримання останньої ціни (latest price) для пари валют.

        Параметри:
            base (str): Базова валюта (наприклад, "BTC").
            quote (str): Валюта котирування (наприклад, "USDT").

        Повертає:
            float: Остання ціна для пари base/quote.
                   Якщо дані не знайдено або виникла помилка, повертається None.

        Логіка:
            1. Спроба отримати дані для прямої пари (наприклад, "BTC/USDT").
            2. Якщо пряма пара недоступна, спробувати отримати дані для зворотної пари (наприклад, "USDT/BTC")
               та інвертувати отримане значення (1 / ціна).
        """
        base = base.upper()
        quote = quote.upper()
        direct_symbol = f"{base}/{quote}"
        reversed_symbol = f"{quote}/{base}"

        # Спроба отримати дані для прямої пари
        try:
            ticker = self.client.fetch_ticker(direct_symbol)
            if ticker and ticker.get('last'):
                return ticker.get('last')
        except Exception as e:
            print(f"[{self.name}] Неможливо отримати дані для {direct_symbol}: {e}")

        # Якщо пряма пара недоступна, пробуємо отримати дані для зворотної пари та інвертуємо ціну
        try:
            ticker = self.client.fetch_ticker(reversed_symbol)
            if ticker and ticker.get('last'):
                reversed_price = ticker.get('last')
                return 1 / reversed_price if reversed_price != 0 else None
        except Exception as e:
            print(f"[{self.name}] Неможливо отримати дані для {reversed_symbol}: {e}")

        return None
