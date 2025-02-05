"""
Модуль gate.py
--------------

Цей модуль містить реалізацію класу GateExchange, який відповідає за взаємодію з біржею Gate.io.
Клас наслідується від CexExchange і використовує бібліотеку ccxt для отримання даних з Gate.io.
"""

import ccxt
from .cex_exchange import CexExchange

class GateExchange(CexExchange):
    def __init__(self):
        """
        Ініціалізує об'єкт GateExchange.

        Використовується ccxt для створення клієнта біржі Gate.io.
        У ccxt ця біржа позначається як "gateio". Параметр 'enableRateLimit': True дозволяє
        уникнути перевищення лімітів запитів до API.
        """
        # Створюємо екземпляр ccxt для Gate.io із ввімкненим лімітуванням запитів
        client = ccxt.gateio({'enableRateLimit': True})
        super().__init__('gate', client)
