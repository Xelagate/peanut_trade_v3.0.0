# supported_pairs.py

# Словник SUPPORTED_PAIRS містить інформацію про доступні торгові пари на Uniswap V3
# Ключі словника – це пари типу "BASE/QUOTE" (наприклад, "ETH/USDT"), значення – це параметри пулу цієї пари.

SUPPORTED_PAIRS = {
    "ETH/USDT": {
        "pool_address": "0x4e68Ccd3E89f51C3074ca5072bbAC773960dFa36",  # Адреса пулу Uniswap для пари ETH/USDT
        "token0": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # Адреса токену WETH (первісний ETH)
        "token1": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # Адреса токену USDT
        "decimals_diff": 12,  # Різниця в десяткових знаках між токенами
    },
    "BTC/ETH": {
        "pool_address": "0xCBCdF9626bC03E24f779434178A73a0B4bad62eD",  # Адреса пулу Uniswap для пари BTC/ETH
        "token0": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # Адреса токену WBTC (Wrapped BTC)
        "token1": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756Cc2",  # Адреса токену WETH (первісний ETH)
        "decimals_diff": -10  # Різниця в десяткових знаках між токенами (BTC має 8 знаків, ETH – 18)
    },
    "ETH/SOL": {
        "pool_address": "0x127452F3f9cDc0389b0Bf59ce6131aA3Bd763598",  # Адреса пулу Uniswap для пари ETH/SOL
        "token0": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756Cc2",  # Адреса токену WETH (первісний ETH)
        "token1": "0xD31a59c85aE9D8edEFeC411D448f90841571b89c",  # Приклад адреси для токену SOL
        "decimals_diff": 9  # Різниця в десяткових знаках між токенами
    },
    "BTC/USDT": {
        "pool_address": "0x9Db9e0e53058C89e5B94e29621a205198648425B",  # Адреса пулу Uniswap для пари BTC/USDT
        "token0": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # Адреса токену WBTC (Wrapped BTC)
        "token1": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # Адреса токену USDT
        "decimals_diff": 2,  # Різниця в десяткових знаках між токенами (BTC має 8 знаків, USDT – 6)
    },
    "BTC/USDC": {
        "pool_address": "0x9Db9e0e53058C89e5B94e29621a205198648425B",  # Адреса пулу Uniswap для пари BTC/USDC
        "token0": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # Адреса токену WBTC (Wrapped BTC)
        "token1": "0xa0b86991c6218b36c1d19d4a2e9Eb0cE3606eb48",  # Адреса токену USDC
        "decimals_diff": 2,  # Різниця в десяткових знаках між токенами (BTC має 8 знаків, USDC – 6)
    },
    # Додайте інші пари тут
}

# Словник TOKEN_ADDRESSES містить адреси основних токенів на Ethereum
# Ключі словника – це назви токенів, значення – це їхні адреси в мережі Ethereum.

TOKEN_ADDRESSES = {
    "ETH": "0xc02aaa39b223Fe8D0A0e5C4F27ead9083C756Cc2",  # Адреса WETH (Wrapped ETH)
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # Адреса USDT
    "USDC": "0xa0b86991c6218B36c1d19d4a2e9Eb0cE3606eb48",  # Адреса USDC
    "BTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # Адреса WBTC (Wrapped BTC)
    "SOL": "0xD31a59c85aE9D8edEFeC411D448f90841571b89c",  # Приклад адреси для SOL
}
