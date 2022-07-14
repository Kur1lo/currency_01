from django.contrib import admin
from django.urls import path
from currency.views import first_func

urlpatterns = [
    path('admin/', admin.site.urls),

    path('first_func/', first_func)
]
