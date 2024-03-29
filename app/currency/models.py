from django.db import models
from datetime import datetime


class ContactUs(models.Model):
    email_to = models.EmailField(max_length=254)
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    massage = models.CharField(max_length=500)


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    logo = models.FileField(default='av.png')


class Rate(models.Model):
    base_currency_type = models.CharField(max_length=3)
    currency_type = models.CharField(max_length=3)
    sale = models.DecimalField(max_digits=10, decimal_places=4)
    buy = models.DecimalField(max_digits=10, decimal_places=4)
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE, related_name='rates')
    created = models.CharField(max_length=30, default=f"{datetime.now():%d.%m.%Y}")


class ResponseLog (models.Model):
    response_time = models.CharField(max_length=64)
    request_method = models.CharField(max_length=64)
    query_params = models.CharField(max_length=64)
    ip = models.CharField(max_length=64)
    path = models.CharField(max_length=64)
