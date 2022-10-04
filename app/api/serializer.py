from rest_framework.serializers import ModelSerializer

from currency.models import Rate, Source, ContactUs
# from currency.tasks import send_contact_us_email


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'buy',
            'sale',
            'currency_type',
            'base_currency_type',
            'created',
            'source',
        )


class SourceSerializer(ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'source_url',
            'name',
            'logo',

        )


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            'id',
            'email_to',
            'email_from',
            'subject',
            'massage',

        )

    # def create(self, validated_data):
    #     return send_contact_us_email.delay(self.subject, self.email_from)

    # def create(self, validated_data):
    #     send_contact_us_email.delay(self.subject, self.email_from)
    #     return Comment(**validated_data)
