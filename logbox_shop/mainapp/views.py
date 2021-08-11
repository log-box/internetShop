import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from mainapp.models import ProductCategory, Product

################################

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_deleted=False)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_deleted=False)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_deleted=False, category__is_deleted=False).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_deleted=False, category__is_deleted=False).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_deleted=False, category__is_deleted=False).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_deleted=False, category__is_deleted=False).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_deleted=False, category__is_deleted=False).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_deleted=False, category__is_deleted=False).order_by('price')
####################################


def get_hot_product():
    products = get_products()
    # return random.sample(list(Product.objects.all()), 1)[0]
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


class ProductsView(TemplateView):
    template_name = 'products.html'
    links_menu = get_links_menu()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['general_menu_links'] = getjson('general_menu_links')
        context['title'] = 'Магазин/Продукция'
        context['products_category_menu'] = self.links_menu #ProductCategory.objects.all()
        context['same_products'] = get_same_products(get_hot_product())
        context['hot_product'] = get_hot_product()
        return context


class ProductView(TemplateView):
    template_name = 'product.html'
    links_menu = get_links_menu()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Продукты/{(get_object_or_404(Product, pk=self.kwargs.get("pk"))).short_desc}'
        # context['general_menu_links'] = getjson('general_menu_links')
        context['products_category_menu'] = self.links_menu # ProductCategory.objects.all()
        context['product'] =  get_product(pk=self.kwargs.get("pk")) #,get_object_or_404(Product, pk=self.kwargs.get("pk"))
        return context


class GroupProductsView(ListView):
    template_name = 'groups_products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['general_menu_links'] = getjson('general_menu_links')
        context['products_category_menu'] = ProductCategory.objects.all()
        if self.kwargs.get('slug') == 'products_all':
            category = {
                'name': 'все',
                'href': 'products_all',
            }
            context['title'] = f'Продукты/{category["name"]}'
        else:
            category = get_object_or_404(ProductCategory, href=self.kwargs.get('slug'))
            context['title'] = f'Продукты/{category.name}'
        context['category'] = category

        return context

    def get_queryset(self):
        if self.kwargs.get('slug') == 'products_all':
            products = Product.objects.filter(is_deleted=False).order_by('price')
        else:
            products = Product.objects.filter(category__href=self.kwargs.get('slug'), is_deleted=False)
        return products


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()
        if pk:
            if pk == '0':
                category = {
                'pk': 0,
                'name': 'все'
                }
            products = get_products_orederd_by_price()
        else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)
        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        content = {
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        result = render_to_string(
                'mainapp/includes/inc_products_list_content.html',
                context=content,
                request=request)
        return JsonResponse({'result': result})


