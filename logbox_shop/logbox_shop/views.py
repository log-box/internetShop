import json

from django.shortcuts import render

from mainapp.models import Product
# from mainapp.views import get_products


def getjson(obj):
    with open(f"{obj}.json", "r") as read_file:
        return json.load(read_file)


def index(request):
    title = 'магазин/главная'
    # products = get_products()[:3]
    products = Product.objects.filter(is_deleted=False, category__is_deleted=False)[:3]
    context = {
        # 'general_menu_links': getjson('general_menu_links'),
        'title': title,
        'products': products,
    }
    return render(request, 'index.html', context)


def contacts(request):
    title = 'магазин/контакты'
    context = {
        # 'general_menu_links': getjson('general_menu_links'),
        'title': title,
    }
    return render(request, 'contact.html', context)
