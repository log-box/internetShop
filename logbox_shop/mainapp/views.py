import random

from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView

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
        context = super().get_context_data(**kwargs)
        context['general_menu_links'] = getjson('general_menu_links')
        context['title'] = 'Магазин/Продукция'
        context['products_category_menu'] = ProductCategory.objects.all()
        context['same_products'] = get_same_products(get_hot_product())
        context['hot_product'] = get_hot_product()
        context['basket'] = get_basket(self.request.user)
        return context


class ProductView(TemplateView):
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Продукты/{(get_object_or_404(Product, pk=self.kwargs.get("pk"))).short_desc}'
        context['general_menu_links'] = getjson('general_menu_links')
        context['products_category_menu'] = ProductCategory.objects.all()
        context['product'] = get_object_or_404(Product, pk=self.kwargs.get("pk")),
        context['basket'] = get_basket(self.request.user)
        return context


class GroupProductsView(ListView):
    template_name = 'groups_products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['general_menu_links'] = getjson('general_menu_links')
        context['products_category_menu'] = ProductCategory.objects.all()
        basket = []
        if self.request.user.is_authenticated:
            basket = get_basket(self.request.user)
        context['basket'] = basket
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
