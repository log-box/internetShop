from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from basketapp.models import Basket
from logbox_shop.views import getjson
from mainapp.models import Product


def basket(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        context = {
            'basket': basket,
            'general_menu_links': getjson('general_menu_links'),
        }
        return render(request, 'basketapp/basket.html', context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    return render(request, 'basketapp/basket.html')
