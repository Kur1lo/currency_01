from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_monobank


def test_parse_mono(mocker):

    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "rateBuy": "411.00000", "rateSell": "411.50000"},
        {"currencyCodeA": 978, "currencyCodeB": 980, "rateBuy": "39.90000", "rateSell": "40.90000"},

    ]

    initial_rate_count = Rate.objects.count()  # 6
    requests_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    parse_monobank()
    assert Rate.objects.count() == initial_rate_count + 2

    parse_monobank()
    assert Rate.objects.count() == initial_rate_count + 2
