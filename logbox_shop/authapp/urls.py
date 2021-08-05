from django.urls import path

from .views import *

app_name = 'authapp'

urlpatterns = [
    path('login/', ShopLoginView.as_view(), name='login'),
    path('logout/', ShopLogoutView.as_view(), name='logout'),
    path('register/', ShopRegisterView.as_view(), name='register'),
    path('edit/', ShopUpdateView.as_view(), name='edit'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]