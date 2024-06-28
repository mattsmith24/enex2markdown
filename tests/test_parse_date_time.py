import enex_parser
from datetime import datetime, timezone

def test_parse_date_time():
    assert enex_parser.parseDateTime("20100203T040506Z") == datetime(2010, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    assert enex_parser.parseDateTime("20240628T171400Z") == datetime(2024, 6, 28, 17, 14, 0, tzinfo=timezone.utc)
