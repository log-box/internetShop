from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('product/<int:pk>/ajax/', cache_page(3600)(products_ajax)),
    path('<slug:slug>/', GroupProductsView.as_view(), name='group_of_products'),
    path('<slug:slug>/page/<int:page>/', GroupProductsView.as_view(), name='page'),
    path('product/<int:pk>/page/<int:page>/ajax/', products_ajax),
    path('product/<int:pk>/', ProductView.as_view(), name='product'),
]
