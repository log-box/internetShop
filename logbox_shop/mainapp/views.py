import random

from django.shortcuts import render

from logbox_shop.views import getjson
from mainapp.models import ProductCategory, Product


def products(request):
    title = 'магазин/продукция'
    products_category = ProductCategory.objects.all()
    # вычислям длину (кол-во) продуктов всего для рандомного числа в этом диапазоне
    len = Product.objects.all().__len__()
    rand_start = random.randint(0, len)
    rand_end = random.randint(0, len)
    if rand_start > rand_end:
        rand_start, rand_end = rand_end, rand_start
    ###############################################################################
    # Берем из базы рандомное число продуктов в переменную proucts и передаем ее в контекст для отображения
    products = Product.objects.all()[rand_start:rand_end]
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        'products_category': products_category,
        'products': products,
    }
    #######################################################################################################
    return render(request, 'products.html', context)


def group_of_products(request, slug):
    title = f'магазин/продукция/{slug}'
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
    }
    return render(request, f'{slug}.html', context)
