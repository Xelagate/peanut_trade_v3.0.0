"""
Модуль binance.py
-----------------

Цей модуль містить реалізацію класу BinanceExchange, який наслідується від CexExchange.
Клас BinanceExchange використовує бібліотеку ccxt для взаємодії з API біржі Binance.
"""

import ccxt
from .cex_exchange import CexExchange

class BinanceExchange(CexExchange):
    def __init__(self):
        """
        Ініціалізує об'єкт BinanceExchange.

        Використовується клієнт ccxt для Binance із ввімкненим лімітуванням запитів
        ('enableRateLimit': True), що допомагає уникнути перевищення обмежень API.
        """
        client = ccxt.binanceus({'enableRateLimit': True})
        super().__init__('binance', client)

