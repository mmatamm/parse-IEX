import pytest

from datetime import datetime

from parse_iex import tops

def test_quote_update_str():
    quote_update = tops.QuoteUpdate('ZIEXT', datetime(2016, 8, 23, 19, 30, 32, 572716), 99.05, 9700, 99.07, 1000)

    assert str(quote_update) == 'best bid: 9700 ZIEXT shares for 99.05 USD; best ask: 1000 ZIEXT shares for 99.07 USD @ 2016-08-23 19:30:32.572716'

def test_trade_report_str():
    trade_report = tops.TradeReport('ZIEXT', datetime(2016, 8, 23, 19, 31, 23, 662975), 99.05, 100)

    assert str(trade_report) == 'trade: 100 ZIEXT shares for 99.05 USD @ 2016-08-23 19:31:23.662975'

def test_decode_quote_update():
    message = b'\x51\x00\xac\x63\xc0\x20\x96\x86\x6d\x14\x5a\x49\x45\x58\x54\x20\x20\x20\xe4\x25\x00\x00\x24\x1d\x0f\x00\x00\x00\x00\x00\xec\x1d\x0f\x00\x00\x00\x00\x00\xe8\x03\x00\x00'
    
    session = tops.Session()
    quote_update = session.decode_message(message)

    assert quote_update.symbol == 'ZIEXT'
    assert quote_update.time == datetime(2016, 8, 23, 19, 30, 32, 572716)
    assert quote_update.bid_price == pytest.approx(99.05)
    assert quote_update.bid_size == 9700
    assert quote_update.ask_price == pytest.approx(99.07)
    assert quote_update.ask_size == 1000

def test_decode_trade_report():
    message = b'\x54\x00\xc3\xdf\xf7\x05\xa2\x86\x6d\x14\x5a\x49\x45\x58\x54\x20\x20\x20\x64\x00\x00\x00\x24\x1d\x0f\x00\x00\x00\x00\x00\x96\x8f\x06\x00\x00\x00\x00\x00'
    
    session = tops.Session()
    trade_report = session.decode_message(message)

    assert trade_report.symbol == 'ZIEXT'
    assert trade_report.time == datetime(2016, 8, 23, 19, 31, 23, 662975)
    assert trade_report.price == pytest.approx(99.05)
    assert trade_report.size == 100