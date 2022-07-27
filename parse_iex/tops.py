from datetime import datetime
import struct

"""
The amount of seconds in a nanosecond
"""
NSEC_TO_SEC = 1 / 1000000000

class QuoteUpdate:
    def __init__(
        self,
        symbol: str,
        time: datetime,
        bid_price: float,
        bid_size: int,
        ask_price: float,
        ask_size: int
    ):
        self.symbol = symbol
        self.time = time
        self.bid_price = bid_price
        self.bid_size = bid_size
        self.ask_price = ask_price
        self.ask_size = ask_size
    
    def from_body(body: bytes):
        # Seperate the buffer to fields
        data = struct.unpack('<BQ8sIQQI', body)

        symbol = data[2].rstrip().decode()
        time = datetime.utcfromtimestamp(data[1] * NSEC_TO_SEC)
        # The price is stored as a fixed-point no.
        bid_price, ask_price = data[4] * 0.0001, data[5] * 0.0001
        bid_size, ask_size = data[3], data[6]

        return QuoteUpdate(symbol, time, bid_price, bid_size, ask_price, ask_size)

class TradeReport:
    def __init__(
        self,
        symbol: str,
        time: datetime,
        price: float,
        size: int
    ):
        self.symbol = symbol
        self.time = time
        self.price = price
        self.size = size
    
    def from_body(body: bytes):
        # Seperate the buffer to fields
        data = struct.unpack('<BQ8sIQq', body)
        
        symbol = data[2].rstrip().decode()
        time = datetime.utcfromtimestamp(data[1] * NSEC_TO_SEC)
        # The price is stored as a fixed-point no.
        price = data[4] * 0.0001
        size = data[3]

        return TradeReport(symbol, time, price, size)