import os
import json
import asyncio
from web3 import Web3
from web3.providers.legacy_websocket import LegacyWebSocketProvider
from dotenv import load_dotenv
from .base import Exchange
from supported_pairs import SUPPORTED_PAIRS, TOKEN_ADDRESSES

load_dotenv()

# Завантаження ABI Uniswap V3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABI_PATH = os.path.join(BASE_DIR, "..", "abi", "uniswap_v3.json")
with open(ABI_PATH, "r") as f:
    ABI = json.load(f)


class UniswapExchange(Exchange):
    """
    Клас для роботи з Uniswap V3 через WebSocket підключення. Використовує події Swap для отримання цін.
    """

    def __init__(self):
        """
        Ініціалізація класу. Підключення до WebSocket через Infura для роботи з Uniswap.
        """
        super().__init__("uniswap")
        infura_project_id = os.getenv("INFURA_PROJECT_ID")
        self.w3 = Web3(LegacyWebSocketProvider(f"wss://mainnet.infura.io/ws/v3/{infura_project_id}"))
        if self.w3.is_connected():
            print("[Uniswap] Підключено до Infura WebSocket")
        else:
            print("[Uniswap] Не вдалося підключитись до Infura WebSocket")
        self.current_price = None
        self.contract = None
        self.pool_info = None
        self.no_events_counter = 0  # Лічильник подій

    async def set_pair(self, pair: str):
        """
        Налаштовує пул для заданої пари. Очищає попередній стан і встановлює новий пул для вказаної пари.

        Параметри:
        pair (str): Назва торгової пари (наприклад, "ETH/USDT").
        """
        # Очищення попереднього стану
        self.current_price = None
        self.contract = None
        self.pool_info = None

        pool_info = SUPPORTED_PAIRS.get(pair.upper())
        if not pool_info:
            print(f"[Uniswap] Пара {pair} не підтримується.")
            return
        self.pool_info = pool_info
        pool_address = Web3.to_checksum_address(pool_info["pool_address"])
        self.contract = self.w3.eth.contract(address=pool_address, abi=ABI)
        print(f"[Uniswap] Пул встановлено для {pair}: {pool_address}")
        # Запускаємо нову підписку
        asyncio.create_task(self._subscribe_to_updates())

    async def _subscribe_to_updates(self):
        """
        Підписка на події Swap, для оновлення поточної ціни.
        Якщо події не надходять протягом тривалого часу, виводиться попередження.
        """
        if not self.contract:
            print("[Uniswap] Контракт не встановлено, неможливо створити фільтр")
            return
        try:
            swap_event = self.contract.events["Swap"]
            event_filter = swap_event.create_filter(from_block="latest")
        except Exception as e:
            print(f"[Uniswap] Помилка створення фільтра: {e}")
            return

        while True:
            try:
                events = event_filter.get_new_entries()
                if events:
                    event = events[0]
                    sqrtPriceX96 = event["args"].get("sqrtPriceX96")
                    if sqrtPriceX96:
                        raw_price = (sqrtPriceX96 / (2 ** 96)) ** 2
                        multiplier = 10 ** self.pool_info.get("decimals_diff", 1)
                        # Обчислюємо ціну
                        self.current_price = raw_price * multiplier
                        print(f"[Uniswap] Оновлено ціну: {self.current_price}")
                    self.no_events_counter = 0  # Скидаємо лічильник при отриманні події
                else:
                    self.no_events_counter += 1
                    if self.no_events_counter >= 10:  # 10 ітерацій без подій
                        print("[Uniswap] Події не отримано за довгий час")
                        self.no_events_counter = 0  # Скидаємо лічильник
                await asyncio.sleep(5)
            except Exception as e:
                print(f"[Uniswap] Помилка прослуховування: {e}")
                await asyncio.sleep(5)

    async def fetch_last_event(self) -> float:
        """
        Отримує останній лог за останніх 500 блоків та повертає обчислену ціну.

        Повертає:
        - float: ціна на основі останнього Swap event або None, якщо події не знайдено.
        """
        try:
            swap_event = self.contract.events["Swap"]
            current_block = self.w3.eth.block_number
            logs = swap_event.get_logs(from_block=current_block - 500, to_block=current_block)
            if logs:
                last_event = logs[-1]
                sqrtPriceX96 = last_event["args"].get("sqrtPriceX96")
                if sqrtPriceX96:
                    raw_price = (sqrtPriceX96 / (2 ** 96)) ** 2
                    multiplier = 10 ** self.pool_info.get("decimals_diff", 1)
                    return raw_price * multiplier
            return None
        except Exception as e:
            print(f"[Uniswap] Помилка отримання історичних логів: {e}")
            return None

    async def get_latest_price(self, base: str, quote: str) -> float:
        """
        Повертає останню отриману ціну для заданої пари.
        Якщо прямий запис не знайдено, шукається зворотній і результат інвертується.

        Параметри:
        - base (str): базова валюта.
        - quote (str): валюта, в яку конвертируется base.

        Повертає:
        - float: ціна за запитом.
        """
        base = base.upper()
        quote = quote.upper()
        pair_key = f"{base}/{quote}"
        pool_info = SUPPORTED_PAIRS.get(pair_key)
        invert_result = False
        if not pool_info:
            reverse_pair = f"{quote}/{base}"
            pool_info = SUPPORTED_PAIRS.get(reverse_pair)
            if pool_info:
                invert_result = True
                pair_key = reverse_pair
            else:
                print(f"[Uniswap] Пара {base}/{quote} не підтримується.")
                return None

        if not self.pool_info or self.pool_info.get("pool_address").lower() != pool_info.get("pool_address",
                                                                                             "").lower():
            await self.set_pair(pair_key)
            await asyncio.sleep(5)

        if self.current_price is None:
            computed_price = await self.fetch_last_event()
            if computed_price is not None:
                self.current_price = computed_price
                print(f"[Uniswap] Історична ціна: {computed_price}")
            else:
                print("[Uniswap] Даних немає.")
                return None

        # Отримуємо адреси токенів з TOKEN_ADDRESSES
        base_addr = TOKEN_ADDRESSES.get(base)
        quote_addr = TOKEN_ADDRESSES.get(quote)
        if not base_addr or not quote_addr:
            print(f"[Uniswap] Невідомі токени: {base} або {quote}")
            return None
        base_addr = Web3.to_checksum_address(base_addr)
        quote_addr = Web3.to_checksum_address(quote_addr)

        token0 = self.pool_info.get("token0").lower()
        token1 = self.pool_info.get("token1").lower()

        if base_addr.lower() == token0 and quote_addr.lower() == token1:
            result = self.current_price  # Це 1 ETH = X USDT
        elif base_addr.lower() == token1 and quote_addr.lower() == token0:
            result = 1 / self.current_price if self.current_price and self.current_price != 0 else None
        else:
            print(f"[Uniswap] Пара токенів не співпадає для {pair_key}")
            return None

        return result
