from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('sing_up/', views.SingUpView.as_view(), name='sing_up'),
    path('activate/<uuid:username>/', views.UserActivateView.as_view(), name='user_activate'),
]
