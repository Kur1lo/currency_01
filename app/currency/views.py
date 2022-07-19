from django.http import HttpResponse
from currency.models import ContactUs


def first_func(request):
    return HttpResponse("Hello world")


def contact_base(request):
    base_list = []
    for data in ContactUs.objects.all():
        redy_string = f'<br>{data.id}, {data.email_to}, {data.email_from}, {data.subject}, {data.massage} '
        base_list.append(redy_string)
    return HttpResponse(str(base_list))
