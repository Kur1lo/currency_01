from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from currency.models import ContactUs, Rate, Source
from currency.forms import RateForm, SourceForm


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


def rate_create(request):
    if request.method == "POST":

        form = RateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/rate/")
    elif request.method == "GET":
        form = RateForm(request.GET)
    context = {"form": form}
    return render(request, 'for_create.html', context=context)


def rate_update(request, rate_id):

    rate_instance = get_object_or_404(Rate, id=rate_id)

    if request.method == "POST":
        form = RateForm(request.POST, instance=rate_instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/rate/")
    elif request.method == "GET":
        form = RateForm(request.GET, instance=rate_instance)

    context = {"form": form}
    return render(request, 'for_update.html', context=context)


def rate_details(request, rate_id):
    rate_instance = get_object_or_404(Rate, id=rate_id)
    context = {'instance': rate_instance}
    return render(request, 'for_details.html', context=context)


def rate_delete(request, rate_id):
    rate_instance = get_object_or_404(Rate, id=rate_id)

    if request.method == 'POST':
        rate_instance.delete()
        return HttpResponseRedirect('/rate/')
    context = {'instance': rate_instance}
    return render(request, 'for_delete.html', context=context)


def source_data(request):
    context = {
        'source_list': Source.objects.all(),
    }
    return render(request, 'source_data.html', context=context)


def source_create(request):
    if request.method == "POST":

        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/source/")
    elif request.method == "GET":
        form = SourceForm(request.GET)
    context = {"form": form}
    return render(request, 'for_create.html', context=context)


def source_update(request, rate_id):

    source_instance = get_object_or_404(Source, id=rate_id)

    if request.method == "POST":
        form = SourceForm(request.POST, instance=source_instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/source/")
    elif request.method == "GET":
        form = SourceForm(request.GET, instance=source_instance)

    context = {"form": form}
    return render(request, 'for_update.html', context=context)


def source_delete(request, rate_id):
    source_instance = get_object_or_404(Source, id=rate_id)

    if request.method == 'POST':
        source_instance.delete()
        return HttpResponseRedirect('/source/')
    context = {'instance': source_instance}
    return render(request, 'for_delete.html', context=context)
