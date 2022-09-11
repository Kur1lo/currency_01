from django.contrib.auth import get_user_model
from django import forms
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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


class RateListView(generic.ListView):
    queryset = Rate.objects.all().select_related('source')
    template_name = 'rate_list.html'


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
