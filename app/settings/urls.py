from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from currency import views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('auth/', include('django.contrib.auth.urls')),

    path('', views.IndexView.as_view(), name='index'),
    path('silk/', include('silk.urls', namespace='silk')),

    path('currency/', include('currency.urls')),
    path('accounts/', include('accounts.urls')),

]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
