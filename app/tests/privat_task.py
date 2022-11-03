from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_privatbank


def test_parse_privatbank(mocker):

    # Rate.objects
    response_json = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "411.00000", "sale": "411.50000"},
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "39.90000", "sale": "40.90000"},
        {"ccy": "BTC", "base_ccy": "USD", "buy": "17668.2920", "sale": "19528.1122"},
    ]

    initial_rate_count = Rate.objects.count()  # 6
    requests_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    parse_privatbank()
    assert Rate.objects.count() == initial_rate_count + 3

    parse_privatbank()
    assert Rate.objects.count() == initial_rate_count + 3
