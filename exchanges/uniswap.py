# exchanges/uniswap.py
from .base import Exchange

class UniswapExchange(Exchange):
    def __init__(self):
        super().__init__('uniswap')
        # Здесь можно добавить инициализацию Uniswap SDK или подписку на WebSocket

    async def get_latest_price(self, base: str, quote: str) -> float:
        # Заглушка с тестовыми данными
        dummy_prices = {
            ('BTC', 'USDT'): 10500,
            ('USDT', 'BTC'): 1 / 10500,
            ('ETH', 'USDT'): 1500,
            ('USDT', 'ETH'): 1 / 1500,
            ('SOL', 'USDT'): 30,
            ('USDT', 'SOL'): 1 / 30,
        }
        price = dummy_prices.get((base, quote))
        if price is None:
            print(f"[Uniswap] Нет данных для пары {base}/{quote}")
        return price
