from django.urls import path

from .views import *

app_name = 'authapp'

urlpatterns = [
    path('login/', ShopLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]