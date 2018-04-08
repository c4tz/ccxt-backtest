# ccxt-backtest

## Features

Currently, only `fetch_ohlcv()` is implemented, but more methods, such as `createOrder()` shall follow.

This has no real exception handling yet, as it is still a WIP project.

## Installation

```shell
$ pip install -U git+https://github.com/c4tz/ccxt-backtest@master#egg=backtest
```

## Usage

In this example, we will fetch an hour of data from Binance's ETH/BTC market and print 10 `5m` candles.

```python
exchange = backtest(
    ccxt.binance(),
    '01-01-2018 13:00',
    '01-01-2018 14:00',
    ['ETH/BTC']
)
for i in range (0, 10): # this is what your bot/strategy would do
    print(exchange.fetch_ohlcv(symbol='ETH/BTC', timeframe='5m', limit=1))
```

Please be aware that you cannot print more than 60 `1m` candles or 4 `15m` candls in this case, because you only have so much data. The candles can also be fetched as one big list, just set up the limit:

```python
print(exchange.fetch_ohlcv(symbol='ETH/BTC', timeframe='1m', limit=60))
```

You could also leave out the markets, which will default to all available BTC markets of the exchange.

**Warning:** Fetching a large time span with many markets can take hours or even days, because there is a limit on how much candles can be fetched at once (based on [the one Binance defines](https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#klinecandlestick-data)).

