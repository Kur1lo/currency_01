import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from currency.utils import to_decimal
from currency import model_choices as mch
from currency import consts


@shared_task(autoretry_for=(OSError,), retry_kwargs={'max_retries': 5})
def send_contact_us_email(subject, email_from):
    email_subject = 'ContactUs From Currency Project'
    body = f'''
    Subject From Client: {subject}
    Email: {email_from}
    Wants to contact
    '''

    from time import sleep
    sleep(3)
    send_mail(
        email_subject,
        body,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source

    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'

    response = requests.get(url)
    response.raise_for_status()  # raise error if not ok

    response_data = response.json()

    currency_type_mapper = {
        'UAH': mch.CurrencyType.CURRENCY_TYPE_UAH,
        'USD': mch.CurrencyType.CURRENCY_TYPE_USD,
        'EUR': mch.CurrencyType.CURRENCY_TYPE_EUR,
        'BTC': mch.CurrencyType.CURRENCY_TYPE_BTC,
    }

    source = Source.objects.get_or_create(
        name=consts.CODE_NAME_PRIVATBANK,
        defaults={'source_url': url, 'name': 'PrivatBank'},
    )[0]

    for rate_data in response_data:
        currency_type = rate_data['ccy']
        base_currency_type = rate_data['base_ccy']

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[rate_data['ccy']]
        base_currency_type = currency_type_mapper[rate_data['base_ccy']]

        buy = to_decimal(rate_data['buy'])
        sale = to_decimal(rate_data['sale'])

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
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
            )


@shared_task
def parse_monobank():
    from currency.models import Rate, Source

    url = 'https://api.monobank.ua/bank/currency'

    response = requests.get(url)
    response.raise_for_status()  # raise error if not ok

    response_data = response.json()

    currency_type_mapper = {
        980: mch.CurrencyType.CURRENCY_TYPE_UAH,
        840: mch.CurrencyType.CURRENCY_TYPE_USD,
        978: mch.CurrencyType.CURRENCY_TYPE_EUR,
    }

    source = Source.objects.get_or_create(
        name=consts.CODE_NAME_MONOBANK,
        defaults={'source_url': url, 'name': 'MonoBank'},
    )[0]

    for rate_data in response_data[0:3]:
        currency_type = rate_data['currencyCodeA']
        base_currency_type = rate_data['currencyCodeB']

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[rate_data['currencyCodeA']]
        base_currency_type = currency_type_mapper[rate_data['currencyCodeB']]

        buy = to_decimal(rate_data['rateBuy'])
        sale = to_decimal(rate_data['rateSell'])

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
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
            )


@shared_task
def parse_nbu():
    from currency.models import Rate, Source

    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

    response = requests.get(url)
    response.raise_for_status()  # raise error if not ok

    response_data = response.json()

    currency_type_mapper = {
        980: 'UAH',
        840: 'USD',
        978: 'EUR',
    }

    source = Source.objects.get_or_create(
        name=consts.CODE_NAME_NBU,
        defaults={'source_url': url, 'name': 'NBU'},
    )[0]

    for rate_data in response_data:

        currency_type = rate_data['r030']

        if currency_type not in currency_type_mapper:
            continue
        else:
            currency_type = currency_type_mapper[rate_data['r030']]
        base_currency_type = currency_type_mapper[980]

        buy = to_decimal(rate_data['rate'])
        sale = to_decimal(rate_data['rate'])

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
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
            )


@shared_task
def parse_oshad_bank():
    from currency.models import Rate, Source

    url = 'https://www.oschadbank.ua/currency-rate'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    mid_titles = [tag.get_text() for tag in
                  soup.find_all("span", class_="heading-block-currency-rate__table-txt body-regular")]
    pars_set = mid_titles[6:18]
    usd = [pars_set[1], pars_set[3], pars_set[4]]
    eur = [pars_set[7], pars_set[9], pars_set[10]]
    redy_set = [usd, eur]
    source = Source.objects.get_or_create(
        name=consts.CODE_NAME_OSHAD_BANK,
        defaults={'source_url': url, 'name': 'OshadBank'},
    )[0]

    for rate_data in redy_set:
        currency_type = rate_data[0]
        base_currency_type = "UAH"
        buy = to_decimal(rate_data[2])
        sale = to_decimal(rate_data[1])

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
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
            )


@shared_task
def parse_pumb():
    from currency.models import Rate, Source

    url = 'https://about.pumb.ua/ru/info/currency_converter'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    mid_titles = [tag.get_text() for tag in soup.find_all("table")]
    pars_set = mid_titles[2].split('\n')[7:15]
    usd = [pars_set[0], pars_set[1], pars_set[2]]
    eur = [pars_set[5], pars_set[6], pars_set[7]]
    redy_set = [usd, eur]
    source = Source.objects.get_or_create(
        name=consts.CODE_NAME_PUMB,
        defaults={'source_url': url, 'name': 'Pumb'},
    )[0]

    for rate_data in redy_set:
        currency_type = rate_data[0]
        base_currency_type = "UAH"
        buy = to_decimal(rate_data[2])
        sale = to_decimal(rate_data[1])

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
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
            )


@shared_task
def parse_vkurse():
    from currency.models import Rate, Source

    url = 'http://vkurse.dp.ua/course.json'

    response = requests.get(url)
    response.raise_for_status()
    response_data = response.json()

    currency_type_mapper = {
        'UAH': mch.CurrencyType.CURRENCY_TYPE_UAH,
        'Dollar': mch.CurrencyType.CURRENCY_TYPE_USD,
        'Euro': mch.CurrencyType.CURRENCY_TYPE_EUR,
        'Pln': "pln",

    }

    source = Source.objects.get_or_create(
        name=consts.CODE_NAME_VKURSE,
        defaults={'source_url': url, 'name': 'VkurseDp'},
    )[0]
    # breakpoint()
    for rate_data in response_data:
        currency_type = currency_type_mapper[rate_data]
        base_currency_type = 'UAH'

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[rate_data]
        base_currency_type = 'UAH'

        buy = to_decimal(response_data[rate_data]['buy'])

        sale = to_decimal(response_data[rate_data]['sale'])
        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
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
            )
