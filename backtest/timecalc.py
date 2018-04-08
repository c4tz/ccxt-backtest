
from datetime import datetime

from dateutil.relativedelta import relativedelta

def add_to_timestamp(timestamp, count, timeframe):
    timestamp = datetime.fromtimestamp(timestamp / 1000)
    unit = timeframe[-1]
    if unit is 'm': timestamp += relativedelta(minutes=count)
    if unit is 'h': timestamp += relativedelta(hours=count)
    if unit is 'd': timestamp += relativedelta(days=count)
    if unit is 'w': timestamp += relativedelta(weeks=count)
    if unit is 'M': timestamp += relativedelta(months=count)
    timestamp = int(timestamp.timestamp())
    timestamp = timestamp if timestamp >= 0 else 0 # avoid negative dates
    return timestamp * 1000
