from django.contrib import admin
from .models import Basket
# Register your models here.

from basketapp.models import Basket

admin.site.register(Basket)
