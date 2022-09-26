from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters

from api.filters import RateFilter, SourceFilter, ContactUsFilter
from api.pagination import RatePagination, ContactUsPagination, SourcePagination
from currency.models import Rate, Source, ContactUs
from api.serializer import RateSerializer, SourceSerializer, ContactUsSerializer
from api.throttles import AnonRateModelThrottle, AnonSourceThrottle


class RatesViews(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = RatePagination

    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ['id', 'buy', 'sale']
    throttle_classes = [AnonRateModelThrottle]


class RatesDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class SourcesViews(generics.ListCreateAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    pagination_class = SourcePagination
    throttle_classes = [AnonSourceThrottle]
    filterset_class = SourceFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ['id', 'source_url', 'name']


class ContactsViews(generics.ListCreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    pagination_class = ContactUsPagination
    filterset_class = ContactUsFilter
    filter_backends = [rest_framework_filters.SearchFilter]
    search_fields = ['email_to', 'email_from', 'subject', 'massage']


class ContactsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
