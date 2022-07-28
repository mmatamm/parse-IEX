from datetime import datetime
import struct

class QuoteUpdate:
    """
    A top-quotes update message

    Attributes
    ----------
    symbol : str
        the stock ticker (e.g. 'AAPL')
    time : datetime.datetime
        the time of the update with nanoseconds precision
    bid_price : float
        best quoted bid price in USD
    bid_size : int
        aggregate quoted best bid size
    ask_price : float
        best quoted ask price in USD
    ask_size : int
        aggregate quoted best ask size
    
    Methods
    -------
    from_body(body)
        Decodes a TOPS Quote Update message into a new `QuoteUpdate`.
    """

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
        """
        Decodes a TOPS Quote Update message and returns a new `QuoteUpdate`.

        Parameters
        ----------
        body : bytes
            the raw message sans the Message Type field
        """
        # Seperate the buffer to fields
        data = struct.unpack('<BQ8sIQQI', body)

        symbol = data[2].rstrip().decode()
        time = datetime.utcfromtimestamp(data[1] / 1E9)
        # The price is stored as a fixed-point no.
        bid_price, ask_price = data[4] / 1E4, data[5] / 1E4
        bid_size, ask_size = data[3], data[6]

        return QuoteUpdate(symbol, time, bid_price, bid_size, ask_price, ask_size)

class TradeReport:
    """
    A trade report

    Attributes
    ----------
    symbol : str
        the stock ticker (e.g. 'AAPL')
    time : datetime.datetime
        the time of the trade with nanoseconds precision
    price : float
        the trade execution price in USD
    size : int
        the no. of shares

    
    Methods
    -------
    from_body(body)
        Decodes a TOPS Trade Report message into a new `TradeReport`.
    """

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
        """
        Decodes a TOPS Trade Report message and returns a new `TradeReport`.

        Parameters
        ----------
        body : bytes
            the raw message sans the Message Type field
        """
        # Seperate the buffer to fields
        data = struct.unpack('<BQ8sIQq', body)
        
        symbol = data[2].rstrip().decode()
        time = datetime.utcfromtimestamp(data[1] / 1E9)
        # The price is stored as a fixed-point no.
        price = data[4] / 1E4
        size = data[3]

        return TradeReport(symbol, time, price, size)