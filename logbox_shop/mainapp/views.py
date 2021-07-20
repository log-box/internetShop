import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import ContextMixin, TemplateResponseMixin, TemplateView

from basketapp.models import Basket
from logbox_shop.views import getjson
from mainapp.models import ProductCategory, Product


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


class ProductsView(TemplateView):
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        extra_context = super().get_context_data(**kwargs)
        extra_context['general_menu_links'] = getjson('general_menu_links')
        extra_context['title'] = 'Магазин/Продукция'
        extra_context['general_menu_links'] = ProductCategory.objects.all()
        extra_context['same_products'] = get_same_products(get_hot_product())
        extra_context['hot_product'] = get_hot_product()
        extra_context['basket'] = get_basket(self.request.user)
        return extra_context


def products(request):
    title = 'магазин/продукция'
    hot_product = get_hot_product()
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        'products_category_menu': ProductCategory.objects.all(),
        'same_products': get_same_products(hot_product),
        'hot_product': hot_product,
        'basket': get_basket(request.user),
    }
    return render(request, 'products.html', context)


def product(request, pk):
    title = f'Продукты/{(get_object_or_404(Product, pk=pk)).short_desc}'
    context = {
        'title': title,
        'general_menu_links': getjson('general_menu_links'),
        'products_category_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'product.html', context)


def group_of_products(request, slug, page=2):
    title = f'магазин/продукция/{slug}'
    basket = []
    if request.user.is_authenticated:
        basket = get_basket(request.user)
    if slug == 'products_all':
        products = Product.objects.filter(is_deleted=False).order_by('price')
        category = {
            'name': 'все',
            'href': 'products_all',
        }
    else:
        products = Product.objects.filter(category__href=slug, is_deleted=False)
        category = get_object_or_404(ProductCategory, href=slug)
    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {
        'general_menu_links': getjson('general_menu_links'),
        'title': title,
        'products_category_menu': ProductCategory.objects.all(),
        'products': products_paginator,
        'category': category,
        'basket': basket,
    }
    return render(request, 'groups_products.html', context)
