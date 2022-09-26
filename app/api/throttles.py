from rest_framework.throttling import AnonRateThrottle


class AnonRateModelThrottle(AnonRateThrottle):
    scope = 'rates'


class AnonSourceThrottle(AnonRateThrottle):
    scope = 'sources'
