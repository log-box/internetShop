import random

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from mainapp.models import ProductCategory, Product


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


class ProductsView(TemplateView):
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['general_menu_links'] = getjson('general_menu_links')
        context['title'] = 'Магазин/Продукция'
        context['products_category_menu'] = ProductCategory.objects.all()
        context['same_products'] = get_same_products(get_hot_product())
        context['hot_product'] = get_hot_product()
        return context


class ProductView(TemplateView):
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Продукты/{(get_object_or_404(Product, pk=self.kwargs.get("pk"))).short_desc}'
        # context['general_menu_links'] = getjson('general_menu_links')
        context['products_category_menu'] = ProductCategory.objects.all()
        context['product'] = get_object_or_404(Product, pk=self.kwargs.get("pk")),
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


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


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
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


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
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
