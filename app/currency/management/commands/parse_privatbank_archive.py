from django.core.management.base import BaseCommand
from currency.arhive_rate import parse_url


class Command(BaseCommand):

    def handle(self, *args, **options):
        parse_url()
