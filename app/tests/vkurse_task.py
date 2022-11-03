from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_vkurse


def test_parse_vkurse(mocker):
    response_json = {
        "Dollar": {"buy": "1.80", "sale": "41.20"},
        "Euro": {"buy": "8.90", "sale": "39.20"}
        }

    initial_rate_count = Rate.objects.count()
    requests_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    parse_vkurse()
    assert Rate.objects.count() == initial_rate_count + 2

    parse_vkurse()
    assert Rate.objects.count() == initial_rate_count + 2
