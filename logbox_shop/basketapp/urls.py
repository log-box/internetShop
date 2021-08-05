from django.urls import path
from basketapp.views import *

app_name = 'basketapp'

urlpatterns = [
    path('', BasketView.as_view(), name='view'),
    path('add/<int:pk>', BasketAddView.as_view(), name='add'),
    path('remove/<int:pk>/', BasketRemove.as_view(), name='remove'),
    path('edit/<int:pk>/<int:quantity>/', BasketEditView.as_view(), name='edit'),

]