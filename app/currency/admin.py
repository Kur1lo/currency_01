from django.contrib import admin
from currency.models import Source, ContactUs, Rate

from rangefilter.filters import DateTimeRangeFilter
from import_export.admin import ImportExportModelAdmin


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'source_url',
        'name',
    )


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email_to',
        'email_from',
        'subject',
        'massage',
    )

    readonly_fields = (
        'id',
        'email_to',
        'email_from',
        'subject',
        'massage',
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Rate)
class RateAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'base_currency_type',
        'currency_type',
        'sale',
        'buy',
    )
    readonly_fields = (
        'sale',
        'buy',
    )
    search_fields = (
        'base_currency_type',
        'currency_type',
        'sale',
        'buy',
    )
    list_filter = (
        'base_currency_type',
        ('created', DateTimeRangeFilter),
    )
