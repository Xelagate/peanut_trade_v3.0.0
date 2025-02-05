"""
Модуль kucoin.py
----------------

Цей модуль містить реалізацію класу KuCoinExchange, який відповідає за взаємодію з біржею KuCoin.
Клас наслідується від CexExchange і використовує бібліотеку ccxt для отримання даних з KuCoin.
"""

import ccxt
from .cex_exchange import CexExchange

class KuCoinExchange(CexExchange):
    def __init__(self):
        """
        Ініціалізує об'єкт KuCoinExchange.

        Використовується ccxt для створення клієнта біржі KuCoin із ввімкненим лімітуванням запитів.
        Параметр 'enableRateLimit': True дозволяє уникнути перевищення лімітів API біржі.
        """
        client = ccxt.kucoin({'enableRateLimit': True})
        super().__init__('kucoin', client)
