from django.shortcuts import render
from logbox_shop.views import getjson


def products(request):
    title = 'магазин/продукция'
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        'links_menu': getjson('links_menu'),
    }
    return render(request, 'products.html', context)
