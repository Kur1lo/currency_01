import django_filters
from currency.models import Rate


# gt, gte, lt, lte, [i]exact, isnull, [i]startswith, [i]endswith, [i]contains, date, in
class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'buy': ('gte', 'lte'),  # buy__gte, buy__lte
            'sale': ('gte', 'lte'),  # buy__gte, buy__lte
            'source': ('exact', ),
            'base_currency_type': ('exact', ),
            'currency_type': ('exact', ),
        }
