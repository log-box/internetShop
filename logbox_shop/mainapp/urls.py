from django.urls import path

import mainapp.models
from .views import products, group_of_products, product, ProductsView

app_name = 'mainapp'

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('<slug:slug>/', group_of_products, name='group_of_products'),
    path('<slug:slug>/page/<int:page>/', group_of_products, name='page'),
    path('product/<int:pk>/', product, name='product'),
]
