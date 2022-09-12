from django.contrib.auth import get_user_model
from django import forms
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_filters.views import FilterView

from currency.filters import RateFilter
from currency.models import ContactUs, Rate, Source, ResponseLog
from currency.forms import RateForm, SourceForm, ContactUsForm

from currency.tasks import send_contact_us_email


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ContactBaseView(generic.ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contact_base.html'


class ContactUsCreateView(generic.CreateView):
    queryset = ContactUs.objects.all()
    template_name = 'create_new_massage.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('currency:contact_base')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['massage'].widget = forms.Textarea()
        return form

    def form_valid(self, form):
        response = super().form_valid(form)

        send_contact_us_email.delay(self.object.subject, self.object.email_from)

        return response


class RateListView(FilterView):
    queryset = Rate.objects.all().select_related('source')
    template_name = 'rate_list.html'
    paginate_by = 10
    filterset_class = RateFilter
    page_size_options = ['4', '8', '12', '24', '36']

    def get_context_data(self, *args, **kwargs):
        context: dict = super().get_context_data(*args, **kwargs)
        filters_params = self.request.GET.copy()

        if self.page_kwarg in filters_params:
            del filters_params[self.page_kwarg]

        context['filters_params'] = filters_params.urlencode()
        context['page_size'] = self.get_paginate_by()
        context['page_size_options'] = self.page_size_options

        return context

    def get_paginate_by(self, queryset=None):
        if self.request.GET.get('page_size') in self.page_size_options:
            paginate_by = self.request.GET['page_size']
        else:
            paginate_by = self.paginate_by

        return paginate_by


class RateCreateView(generic.CreateView):
    queryset = Rate.objects.all()
    template_name = 'rate_create-update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


class RateUpdateView(generic.UpdateView):
    queryset = Rate.objects.all()
    template_name = 'rate_create-update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


class RateDeleteView(UserPassesTestMixin, generic.DeleteView):
    queryset = Rate.objects.all()
    template_name = 'for_delete.html'
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        return self.request.user.is_superuser


class RateDetailsView(generic.DeleteView):
    queryset = Rate.objects.all()
    template_name = 'for_details.html'


class SourceDataView(generic.ListView):
    queryset = Source.objects.all()
    template_name = 'source_data.html'


class SourceCreateView(generic.CreateView):
    queryset = Source.objects.all()
    template_name = 'source_create-update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source')


class SourceUpdateView(generic.UpdateView):
    queryset = Source.objects.all()
    template_name = 'source_create-update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source')


class SourceDeleteView(generic.DeleteView):
    queryset = Source.objects.all()
    template_name = 'for_delete.html'
    success_url = reverse_lazy('currency:source')


class ResponseLogView(generic.ListView):
    queryset = ResponseLog.objects.all()
    template_name = 'response_log.html'


class UserProfileView(LoginRequiredMixin, generic.UpdateView):
    queryset = get_user_model().objects.all()
    template_name = 'my_profile.html'
    success_url = reverse_lazy('index')
    fields = (
        'first_name',
        'last_name',
        'avatar',
    )

    def get_object(self, queryset=None):
        return self.request.user
