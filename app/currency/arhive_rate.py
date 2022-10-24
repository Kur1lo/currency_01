# from currency.models import Rate, Source
# from currency import consts
#
# import requests
#
# from currency.utils import to_decimal
#
#
# def parse_url(day, month, year):
#     url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={day}.{month}.{year}"
#     response = requests.get(url)
#     print(response.json())
#     response_data = response.json()
#     write_to_db(response_data, url)
#     return date_for_parse(response)
#
#
# def date_for_parse(response):
#     date = response.json()['date']
#     date_my = []
#
#     for x in date.split('.'):
#         date_my.append(x)
#
#     day = int(date_my[0])
#     month = int(date_my[1])
#     year = int(date_my[2])
#
#     return parse_url(day - 1, month, year)
#
#
# def write_to_db(response_data, url):
#
#     source = Source.objects.get_or_create(
#         name=consts.CODE_NAME_PRIVATBANK,
#         defaults={'source_url': url, 'name': 'PrivatBank'},)[0]
#
#     for rate_data in response_data['exchangeRate'][1:]:
#         currency_type = rate_data['currency']
#         base_currency_type = rate_data['baseCurrency']
#
#         buy = to_decimal(rate_data['purchaseRateNB'])
#         sale = to_decimal(rate_data['saleRateNB'])
#         created = response_data['date']
#
#         try:
#             latest_rate = Rate.objects.filter(
#                 base_currency_type=base_currency_type,
#                 currency_type=currency_type,
#                 source=source,
#             ).latest('created')
#         except Rate.DoesNotExist:
#             latest_rate = None
#
#         if latest_rate is None or \
#                 latest_rate.sale != sale or \
#                 latest_rate.buy != buy:
#             Rate.objects.create(
#                 base_currency_type=base_currency_type,
#                 currency_type=currency_type,
#                 buy=buy,
#                 sale=sale,
#                 source=source,
#             )
#
#
# def start_parse():
#     for _ in range(5):
#         parse_url(17, 10, 2022)
