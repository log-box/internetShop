from django.urls import path

from .users_views.users import UserCreateView, UsersListView, UserUpdateView, user_delete
from .views import  category_create, categories, category_update, \
    category_delete, product_delete, product_update, product_create, product_read, products
app_name = 'adminapp'

urlpatterns = [
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    # path('users/read/', users, name='users'),
    path('users/read/', UsersListView.as_view(), name='users'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', user_delete, name='user_delete'),

    path('categories/create/', category_create, name='category_create'),
    path('categories/read/', categories, name='categories'),
    path('categories/update/<int:pk>/', category_update, name='category_update'),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),

    path('products/create/category/<int:pk>/', product_create, name='product_create'),
    path('products/read/category/<int:pk>/', products, name='products'),
    path('products/read/<int:pk>/', product_read, name='product_read'),
    path('products/update/<int:pk>/', product_update, name='product_update'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
]
