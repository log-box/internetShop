import json
from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def getjson(obj):
    with open(f"{obj}.json", "r") as read_file:
        return json.load(read_file)


def index(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    title = 'магазин/главная'
    products = Product.objects.all()[:3]

    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        'products': products,
        'basket': basket,
    }
    return render(request, 'index.html', context)


def contacts(request):
    title = 'магазин/контакты'
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
    }
    return render(request, 'contact.html', context)
