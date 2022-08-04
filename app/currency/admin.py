from django.contrib import admin
from currency.models import Source, ContactUs


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

