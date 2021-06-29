from django.shortcuts import render
from logbox_shop.views import getjson
from mainapp.models import ProductCategory


def products(request):
    title = 'магазин/продукция'
    products_category = ProductCategory.objects.all()
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        # 'links_menu': getjson('links_menu'),
        'products_category': products_category,
    }
    return render(request, 'products.html', context)
