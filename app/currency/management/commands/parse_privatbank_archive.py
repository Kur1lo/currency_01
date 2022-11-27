from django.core.management.base import BaseCommand
from currency.arhive_rate import parse_url

from datetime import datetime

DATE = f"{datetime.now():%d.%m.%Y}".split('.')


class Command(BaseCommand):

    def handle(self, *args, **options):
        parse_url(day=DATE[0], month=DATE[1], year=DATE[2])
