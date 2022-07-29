from django.http import HttpResponse
from django.shortcuts import render

from currency.models import ContactUs, Rate, Source


def first_func(request):
    return HttpResponse("Hello world")


def index(request):
    return render(request, 'index.html')


def contact_base(request):
    context = {
        'base_list': ContactUs.objects.all(),
    }
    return render(request, 'contact_base.html', context=context)


def rate_list(request):
    context = {
        'rate_list': Rate.objects.all(),
    }
    return render(request, 'rate_list.html', context=context)


def source_data(request):
    context = {
        'rate_list': Source.objects.all(),
    }
    return render(request, 'source_data.html', context=context)
