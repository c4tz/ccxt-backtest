import ccxt

from dateutil.parser import parse
from data import data
from timecalc import add_to_timestamp

class backtest(ccxt.Exchange):

    def __init__(self, exchange: ccxt.Exchange, since: str, to: str, markets: list = []):
        # copy all properties from original exchange
        #self.__dict__.update(exchange.__dict__)
        self.markets = markets
        self.rateLimit = exchange.rateLimit
        self.name = exchange.name
        self.exchange = exchange

        since=int(parse(since).timestamp())*1000
        to=int(parse(to).timestamp())*1000

        self.data = data(self.exchange)
        self.data.load_candles(
            markets=self.markets,
            since=since,
            to=to
        )
        self.timestamp = since

    def fetch_ohlcv(self, symbol, timeframe = '1m', since = None, limit = None, params = {}):
        if not since:
            since = self.timestamp
        self.timestamp = add_to_timestamp(since, limit, timeframe)
        return self.data.get_candles(
            market=symbol,
            timestamp=since,
            limit=limit,
            timeframe=timeframe
        )

    def load_markets(self):
        return self.markets
