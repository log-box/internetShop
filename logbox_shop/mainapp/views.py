import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from logbox_shop.views import getjson
from mainapp.models import ProductCategory, Product


def products(request):
    title = 'магазин/продукция'
    products_category_menu = ProductCategory.objects.all()
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    # вычислям длину (кол-во) продуктов всего для рандомного числа в этом диапазоне
    _len = Product.objects.all().__len__()
    rand_start = random.randint(0, _len)
    rand_end = random.randint(0, _len)
    if rand_start > rand_end:
        rand_start, rand_end = rand_end, rand_start
    ###############################################################################
    # Берем из базы рандомное число продуктов в переменную proucts и передаем ее в контекст для отображения
    products = Product.objects.all()[rand_start:rand_end]
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        'products_category_menu': products_category_menu,
        'products': products,
        'basket': basket,
    }
    #######################################################################################################
    return render(request, 'products.html', context)


def group_of_products(request, slug):
    title = f'магазин/продукция/{slug}'
    products_category_menu = ProductCategory.objects.all()
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    if slug == 'products_all':
        products = Product.objects.all().order_by('price')
        category = {'name': 'все'}
    else:
        products = Product.objects.filter(category__href=slug).order_by('price')
        category = get_object_or_404(ProductCategory, href=slug)
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        'products_category_menu': products_category_menu,
        'products': products,
        'category': category,
        'basket': basket,
    }
    return render(request, 'groups_products.html', context)
