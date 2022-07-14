from django.http import HttpResponse


def first_func(request):
    return HttpResponse('Hello World')
