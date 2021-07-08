from django.urls import path

import mainapp.models
from .views import products, group_of_products, product

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='products'),
    path('<slug:slug>/', group_of_products, name='group_of_products'),
    path('product/<int:pk>/', product, name='product'),
]
