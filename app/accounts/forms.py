import uuid

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse

from accounts.models import User


class SingUpForm(forms.ModelForm):
    password_1 = forms.CharField(widget=forms.PasswordInput())
    password_2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password_1',
            'password_2',
                  )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email.lower()

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password_1'] != cleaned_data['password_2']:
                raise forms.ValidationError('Passwords missmatch!')

        return cleaned_data

    def save(self, commit=True):
        instance: User = super().save(commit=False)
        instance.username = str(uuid.uuid4())
        instance.is_active = False
        instance.set_password(self.cleaned_data['password_1'])
        if commit:
            instance.save()
        self._send_activation_email()

        return instance

    def _send_activation_email(self):
        subject = 'Activate your account'
        body = f'''
        Activation link: {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:user_activate',
                                                                            args=(self.instance.username,))}
        '''

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [self.instance.email],
            fail_silently=False,
        )
