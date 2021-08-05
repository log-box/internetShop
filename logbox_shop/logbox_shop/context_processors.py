import json

from basketapp.models import Basket
from mainapp.models import Product


def getjson(obj):
    with open(f"{obj}.json", "r") as read_file:
        return json.load(read_file)


def basket(request):
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    return {
        'basket': basket,
    }


def menu(request):
    return {
        'general_menu_links': getjson('general_menu_links'),
    }