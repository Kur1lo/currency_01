from django.urls import path
from currency import views

app_name = 'currency'

urlpatterns = [

    path('rate/', views.RateListView.as_view(), name='rate_list'),
    path('rate/rate_create/', views.RateCreateView.as_view(), name='rate_create'),
    path('rate/update/<int:pk>/', views.RateUpdateView.as_view(), name='rate_update'),
    path('rate/delete/<int:pk>/', views.RateDeleteView.as_view(), name='rate_delete'),
    path('rate/details/<int:pk>/', views.RateDetailsView.as_view(), name='rate_details'),

    path('contact_base/', views.ContactBaseView.as_view(), name='contact_base'),
    path('contact_base/create/', views.ContactUsCreateView.as_view(), name='base_create'),

    path('source/', views.SourceDataView.as_view(), name='source'),
    path('source/create/', views.SourceCreateView.as_view(), name='source_create'),
    path('source/update/<int:pk>/', views.SourceUpdateView.as_view(), name='source_update'),
    path('source/delete/<int:pk>/', views.SourceDeleteView.as_view(), name='source_delete'),

    path('response_log/', views.ResponseLogView.as_view(), name='response_log')
]
