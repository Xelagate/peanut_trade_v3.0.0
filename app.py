"""
Модуль app.py
-------------

Цей файл містить основний код FastAPI додатку для агрегування даних з криптобірж.
Реалізовано два ендпоінти:
    1. /estimate  - визначає, на якій біржі найбільш вигідно здійснити обмін,
                    повертає назву біржі та суму, яку отримаємо після обміну.
    2. /getRates  - повертає котирування для заданої пари (baseCurrency/quoteCurrency)
                    з усіх підтримуваних бірж.

Архітектура побудована таким чином, що для кожної біржі реалізовано клас, який має
метод get_latest_price для отримання останньої ціни. Додаток агрегує дані з усіх бірж.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio

# Імпортуємо класи бірж
from exchanges.binance import BinanceExchange
from exchanges.kucoin import KuCoinExchange
from exchanges.uniswap import UniswapExchange
from exchanges.raydium import RaydiumExchange
from exchanges.gate import GateExchange

# Ініціалізація FastAPI додатку
app = FastAPI(title="Crypto Exchange API", version="1.0")

# Ініціалізація об'єктів бірж
binance = BinanceExchange()
kucoin = KuCoinExchange()
gate = GateExchange()
uniswap = UniswapExchange()
raydium = RaydiumExchange()

# Об'єднуємо всі біржі в один список для подальшої обробки
exchanges = [binance, kucoin, gate, uniswap, raydium]

app.mount("/static", StaticFiles(directory="static"), name="static")

# Моделі запитів, що використовуються для валідації вхідних даних через Pydantic

class EstimateRequest(BaseModel):
    """
    Модель запиту для ендпоінту /estimate.

    Атрибути:
        inputAmount: Сума, яку хоче обміняти користувач.
        inputCurrency: Валюта, яку користувач хоче обміняти (наприклад, "BTC").
        outputCurrency: Валюта, яку користувач хоче отримати (наприклад, "USDT").
    """
    inputAmount: float
    inputCurrency: str
    outputCurrency: str


class GetRatesRequest(BaseModel):
    """
    Модель запиту для ендпоінту /getRates.

    Атрибути:
        baseCurrency: Базова валюта для котирування (наприклад, "BTC").
        quoteCurrency: Валюта котирування (наприклад, "ETH").
    """
    baseCurrency: str
    quoteCurrency: str


async def fetch_prices(base: str, quote: str):
    """
    Асинхронна функція для отримання котирувань з усіх бірж.

    Параметри:
        base (str): Базова валюта.
        quote (str): Валюта котирування.

    Повертає:
        Список кортежів (назва_біржі, ціна) для кожної біржі.
    """
    # Створюємо список завдань для отримання котирувань з кожної біржі
    tasks = [exchange.get_latest_price(base, quote) for exchange in exchanges]
    prices = await asyncio.gather(*tasks)
    return list(zip([ex.name for ex in exchanges], prices))


async def estimate(input_amount: float, input_currency: str, output_currency: str):
    """
    Асинхронна функція для визначення найбільш вигідного обміну.

    Параметри:
        input_amount (float): Сума, яку користувач хоче обміняти.
        input_currency (str): Валюта, яку користувач хоче обміняти.
        output_currency (str): Валюта, яку користувач хоче отримати.

    Повертає:
        Кортеж (best_exchange, best_output_amount), де:
            best_exchange - назва біржі, що дає найкращий курс,
            best_output_amount - сума, яку отримаємо після обміну.
    """
    best_exchange = None
    best_output_amount = -1
    # Отримуємо котирування з усіх бірж
    results = await fetch_prices(input_currency, output_currency)
    # Проходимо по результатах і знаходимо найвигідніший обмін
    for name, price in results:
        if price is None:
            continue
        output_amount = input_amount * price
        if output_amount > best_output_amount:
            best_output_amount = output_amount
            best_exchange = name
    return best_exchange, best_output_amount


@app.post("/estimate")
async def estimate_endpoint(request: EstimateRequest):
    """
    Ендпоінт /estimate.

    Приймає JSON запит, який містить:
        - inputAmount: Сума обміну.
        - inputCurrency: Валюта, яку обмінюють.
        - outputCurrency: Валюта, яку хочуть отримати.

    Повертає:
        JSON об'єкт з назвами біржі та сумою, яку отримаємо після обміну.

    Якщо не вдалося отримати дані жодної біржі, повертається помилка 500.
    """
    best_exchange, best_output_amount = await estimate(
        request.inputAmount, request.inputCurrency, request.outputCurrency
    )
    if best_exchange is None:
        raise HTTPException(status_code=500, detail="Не вдалося отримати дані ні від однієї біржі")
    return {"exchangeName": best_exchange, "outputAmount": best_output_amount}


@app.post("/getRates")
async def get_rates_endpoint(request: GetRatesRequest):
    """
    Ендпоінт /getRates.

    Приймає JSON запит, який містить:
        - baseCurrency: Базова валюта.
        - quoteCurrency: Валюта котирування.

    Повертає:
        JSON масив об'єктів, де кожен об'єкт містить:
            - exchangeName: Назва біржі.
            - rate: Курс (ціна) 1 базової валюти в quoteCurrency.
            Якщо дані недоступні, повертається повідомлення про помилку.
    """
    results = await fetch_prices(request.baseCurrency, request.quoteCurrency)
    response = []
    for name, price in results:
        if price is None:
            response.append({"exchangeName": name, "error": "Немає даних"})
        else:
            response.append({"exchangeName": name, "rate": price})
    return response


if __name__ == '__main__':
    import uvicorn

    # Запускаємо сервер на 0.0.0.0:8000 з автоматичним перезавантаженням при зміні коду
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
