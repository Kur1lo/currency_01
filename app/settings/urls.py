from django.contrib import admin
from django.urls import path
from currency.views import first_func, contact_base, rate_list, index, source_data, rate_create, rate_update, rate_details, rate_delete

urlpatterns = [
    path('admin/', admin.site.urls),

    path('first_func/', first_func),

    path('contact_base/', contact_base),

    path('rate/', rate_list),

    path('rate/rate_create/', rate_create),

    path('rate/update/<int:rate_id>/', rate_update),

    path('rate/details/<int:rate_id>/', rate_details),

    path('rate/delete/<int:rate_id>/', rate_delete),

    path('source/', source_data),

    path('', index),
]
