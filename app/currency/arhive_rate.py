from json import JSONDecodeError

from currency.utils import to_decimal
from currency.models import Rate, Source
from currency import consts

import requests
from datetime import datetime


DATE = f"{datetime.now():%d.%m.%Y}".split('.')


def parse_url(day=DATE[0], month=DATE[1], year=DATE[2]):
    count = 0
    date_parse = []

    while count != 3:

        day = day if len(date_parse) == 0 else int(date_parse[0]) - 1
        month = month if len(date_parse) == 0 else int(date_parse[1])
        year = year if len(date_parse) == 0 else int(date_parse[2])

        url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={day}.{month}.{year}"

        response = requests.get(url)
        response_data = response.json()
        if len(response_data['exchangeRate']) == 0:
            count += 1
            continue
        else:
            count = 0
            write_to_db(response_data, url)

        date = response.json()['date']
        date_parse.clear()

        for x in date.split('.'):
            date_parse.append(x)


def write_to_db(response_data, url):

    source = Source.objects.get_or_create(
        name=consts.CODE_NAME_PRIVATBANK,
        defaults={'source_url': url, 'name': 'PrivatBank'},)[0]

    for rate_data in response_data['exchangeRate'][1:]:
        try:
            currency_type = rate_data['currency']
            base_currency_type = rate_data['baseCurrency']
            buy = to_decimal(rate_data['purchaseRate'])
            sale = to_decimal(rate_data['saleRate'])
            created = response_data['date']
        except KeyError:
            continue
        except JSONDecodeError:
            continue

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
                created=created,
            ).latest('created')
        except Rate.DoesNotExist:
            latest_rate = None

        if latest_rate is None or \
                latest_rate.sale != sale or \
                latest_rate.buy != buy:
            Rate.objects.create(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                buy=buy,
                sale=sale,
                source=source,
                created=created,
            )
