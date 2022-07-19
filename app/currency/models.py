from django.db import models


class ContactUs(models.Model):
    email_to = models.EmailField(max_length=254)
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    massage = models.CharField(max_length=500)
