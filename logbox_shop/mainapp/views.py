from django.shortcuts import render
import random
from logbox_shop.views import getjson
from mainapp.models import ProductCategory, Product


def products(request):
    title = 'магазин/продукция'
    products_category = ProductCategory.objects.all()
    len = Product.objects.all().__len__()
    rand_start = random.randint(0, len)
    rand_end = random.randint(0, len)
    if rand_start > rand_end:
        rand_start, rand_end = rand_end, rand_start
    products = Product.objects.all()[rand_start:rand_end]
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        # 'links_menu': getjson('links_menu'),
        'products_category': products_category,
        'products': products,
    }
    return render(request, 'products.html', context)


def group_of_products(request, slug):
    title = f'магазин/продукция/{slug}'
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
    }
    return render(request, f'{slug}.html', context)
