from django.urls import reverse_lazy
from django.views import generic

from currency.models import ContactUs, Rate, Source, ResponseLog
from currency.forms import RateForm, SourceForm
from currency.middelewares import SimpleMiddleware


class ContactBaseView(generic.ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contact_base.html'


class RateListView(generic.ListView):
    queryset = Rate.objects.all()
    template_name = 'rate_list.html'


class RateCreateView(generic.CreateView):
    queryset = Rate.objects.all()
    template_name = 'for_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


class RateUpdateView(generic.UpdateView):
    queryset = Rate.objects.all()
    template_name = 'for_update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


class RateDeleteView(generic.DeleteView):
    queryset = Rate.objects.all()
    template_name = 'for_delete.html'
    success_url = reverse_lazy('currency:rate_list')


class RateDetailsView(generic.DeleteView):
    queryset = Rate.objects.all()
    template_name = 'for_details.html'


class SourceDataView(generic.ListView):
    queryset = Source.objects.all()
    template_name = 'source_data.html'


class SourceCreateView(generic.CreateView):
    queryset = Source.objects.all()
    template_name = 'for_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source')


class SourceUpdateView(generic.UpdateView):
    queryset = Source.objects.all()
    template_name = 'for_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source')


class SourceDeleteView(generic.DeleteView):
    queryset = Source.objects.all()
    template_name = 'for_delete.html'
    success_url = reverse_lazy('currency:source')


class ResponseLogView(generic.ListView):
    queryset = ResponseLog.objects.all()
    template_name = 'response_log.html'
