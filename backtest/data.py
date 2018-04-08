import ccxt
import datetime
import itertools
import sqlite3
import os
import time

from timecalc import add_to_timestamp

class data():
    def __init__(self, exchange: ccxt.Exchange):
        self.exchange = exchange
        self.connection = sqlite3.connect(self.exchange.name + '.db')
        self.cursor = self.connection.cursor()

    def fetch_candles(
        self, 
        market: str,
        since: int,
        to: int
    ) -> list:
        limit = 500 # binance has a 500 candle limit
        timeframe = '1m'
        if to is None:
            to = int(datetime.datetime.now().timestamp()) * 1000
        timestamp = add_to_timestamp(to, -limit, timeframe)
        candles = self.exchange.fetch_ohlcv(
            market,
            timeframe=timeframe,
            since=timestamp,
            limit=limit
        )
        if candles[0][0] > since and not candles[0][0] > to: # there seems to be more data
            time.sleep(self.exchange.rateLimit / 1000)
            candles += self.fetch_candles(
                market=market,
                since=since,
                to=timestamp
            )
            candles.sort()
            candles = list(candles for candles,_ in itertools.groupby(candles))
        return candles

    def is_btc_market(self, symbol: str):
        if '/BTC' in symbol:
            return True
        return False

    def save_candles(self, market: str, candles: list):
        for candle in candles:
            try:
                self.cursor.execute(
                    'INSERT INTO ' + market.replace('/', '') + ' VALUES (?,?,?,?,?,?)',
                    candle
                )
            except sqlite3.IntegrityError:
                continue
        self.connection.commit()

    def get_candles(self, market: str, timestamp: int, limit: int, timeframe: str):
        ohlcv = []
        for i in range (0, limit):
            timestamp = add_to_timestamp(timestamp, -i, timeframe)
            since = add_to_timestamp(timestamp, -1, timeframe)
            to = timestamp
            candles = self.cursor.execute(
                ('SELECT * FROM ' + market.replace('/', '') + ' '
                'WHERE timestamp>=? AND timestamp<=?'),
                (since, to)
            ).fetchall()
            open = candles[0][1]
            close = candles[len(candles)-1][4]
            timestamp = candles[len(candles)-1][0]
            high = low = volume = 0
            for candle in candles:
                if candle[2] > high: high = candle[2]
                if candle[3] < low: low = candle[3]
                volume += candle[5]
            ohlcv.append([timestamp, open, high, low, close, volume])
        return ohlcv

    def candles_present(self, market: str, since: int, to: int):
        count = self.cursor.execute(
            ('SELECT COUNT(timestamp) FROM ' + market.replace('/', '') + ' '
            'WHERE timestamp>=? AND timestamp<=?'),
            (since, to)
        ).fetchone()[0]
        difference = int((to - since) / 1000 / 60) # in minutes
        if count < difference:
            return False
        return True

    def load_candles(
        self,
        markets: list = [],
        since: str = '',
        to: str = ''
    ):
        if not markets:
            markets = list(filter(self.is_btc_market, self.exchange.load_markets()))
        for index, market in enumerate(markets):
            print('Importing market "' + market + '" (' + str(index+1) + '/' + str(len(markets)) + ')')
            self.cursor.execute((
                'CREATE TABLE if not exists ' + market.replace('/', '') + ' ('
                'timestamp integer not null primary key, '
                'open integer, '
                'high integer, '
                'low integer, '
                'close integer, '
                'volume integer)'
            ))
            self.connection.commit()
            if not self.candles_present(market, since, to):
                candles = self.fetch_candles(
                    market=market,
                    since=since,
                    to=to
                )
                self.save_candles(market, candles)