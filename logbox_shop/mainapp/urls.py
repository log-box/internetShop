from django.urls import path
from .views import *

app_name = 'mainapp'

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('<slug:slug>/', GroupProductsView.as_view(), name='group_of_products'),
    path('<slug:slug>/page/<int:page>/', GroupProductsView.as_view(), name='page'),
    path('product/<int:pk>/', ProductView.as_view(), name='product'),
]
