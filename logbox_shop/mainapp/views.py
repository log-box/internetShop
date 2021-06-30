import json

from django.shortcuts import render
import random
from logbox_shop.views import getjson
from mainapp.models import ProductCategory, Product



def products(request):
    title = 'магазин/продукция'
    # загружаем меню категорий из json
    # ProductCategory.objects.all().delete()
    # with open("links_menu.json", "r") as read_file:
    #     data = json.load(read_file)
    #     for item in data:
    #         category_name = item['name']
    #         category_href = item['href']
    #         new_category = ProductCategory(name=category_name, href=category_href)
    #         new_category.save()
    ##################################
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
        # 'links_menu': getjson('links_menu'),
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
