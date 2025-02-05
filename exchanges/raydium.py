from .base import Exchange


class RaydiumExchange(Exchange):
    """
    Заглушена реалізація RaydiumExchange для тестування.

    Наразі цей клас не підписується на реальні оновлення через WebSockets/Yellowstone gRPC.
    Метод get_latest_price повертає фіктивне значення для пари SOL/USDT, щоб не заважати перевірці роботи Uniswap.

    Для запиту:
      - SOL/USDT повертається поточна фіктивна ціна (наприклад, 32.0).
      - USDT/SOL повертається інвертована ціна.
    Для інших пар повертається None.
    """

    def __init__(self):
        super().__init__("raydium")
        # Фіктивна ціна для SOL/USDT
        self.current_price = 32.0

    async def get_latest_price(self, base: str, quote: str) -> float:
        """
        Повертає фіктивну ціну для заданої пари валют.

        Підтримуються:
            - SOL/USDT: повертається self.current_price (наприклад, 32.0).
            - USDT/SOL: повертається інвертована ціна.
        Для інших пар повертається None.

        Параметри:
            base (str): Базова валюта.
            quote (str): Валюта котирування.
        """
        base = base.upper()
        quote = quote.upper()
        if base == "SOL" and quote == "USDT":
            return self.current_price
        elif base == "USDT" and quote == "SOL":
            return 1 / self.current_price if self.current_price and self.current_price != 0 else None
        else:
            return None
