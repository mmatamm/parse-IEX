import pytest

from datetime import datetime

from parseiex import iextp

def test_outbound_segment_str():
    outbound_segment = iextp.OutboundSegment([b'Message 1', b'Message 2'], 0xFFFF)

    assert str(outbound_segment) == "IEX-TP outbound segment: [b'Message 1', b'Message 2']"

def test_decode():
    message = b'\x01\x00\xFF\xFF\x01\x00\x00\x00\x00\x00\x87\x42\x07\x00\x02\x00\x8c\xa6\x21\x00\x00\x00\x00\x00\xca\xc3\x00\x00\x00\x00\x00\x00\xec\x45\xc2\x20\x96\x86\x6d\x14\x01\x00\x69\x02\x00\xBE\xEF'
    
    session = iextp.Session()
    outbound_segment = session.decode_packet(message)

    assert outbound_segment.messages == [b'\x69', b'\xBE\xEF']
    assert outbound_segment.messages_protocol_id == 65535 # non-existent protocol
    assert not outbound_segment.past