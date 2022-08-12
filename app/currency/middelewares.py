from time import time
import requests

from currency.models import ResponseLog


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time()

        response = self.get_response(request)

        end = time()

        def resp_time(start, end):
            return str(end - start)

        req_method = request.method
        quer_params = request.META["QUERY_STRING"]
        path = request.path

        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip

        data = ResponseLog(response_time=resp_time(start, end),
                           request_method=req_method,
                           query_params=quer_params,
                           ip=get_client_ip(request),
                           path=path
                           )
        data.save()
        return response
