from django.db import models


class CurrencyType(models.TextChoices):
    CURRENCY_TYPE_UAH = 'UAH', 'Hrivna'
    CURRENCY_TYPE_USD = 'USD', 'Dollar'
    CURRENCY_TYPE_EUR = 'EUR', 'Euro'
    CURRENCY_TYPE_BTC = 'BTC', 'BitCoin'
