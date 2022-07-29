from django.contrib import admin
from django.urls import path
from currency.views import first_func, contact_base, rate_list, index, source_data

urlpatterns = [
    path('admin/', admin.site.urls),

    path('first_func/', first_func),

    path('contact_base/', contact_base),

    path('rate/', rate_list),

    path('source/', source_data),

    path('', index)
]
