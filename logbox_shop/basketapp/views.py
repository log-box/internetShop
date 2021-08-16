from django.contrib.auth.decorators import user_passes_test
from django.db.models import F, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from basketapp.models import Basket
from logbox_shop.views import getjson
from mainapp.models import Product


class BasketView(ListView):
    template_name = 'basketapp/basket.html'
    context_object_name = 'basket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['general_menu_links'] = getjson('general_menu_links')
        return context

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user).order_by('product__name')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BasketAddView(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if 'login' in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('products:product', args=[kwargs['pk']]))
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=kwargs['pk'])
            if product.quantity > 0:
                basket = Basket.objects.filter(user=request.user, product=product).first()
                if not basket:
                    basket = Basket(user=request.user, product=product)
                basket.quantity += 1
                # basket[0].quantity = F('quantity') +1
                basket.save()
                return HttpResponseRedirect(reverse('mainapp:group_of_products', kwargs={'slug': product.category.href}))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketRemove(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        basket_record = get_object_or_404(Basket, pk=kwargs['pk'])
        basket_record.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketEditView(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if request.is_ajax():
            quantity = int(kwargs['quantity'])
            new_basket_item = Basket.objects.get(pk=int(kwargs['pk']))
            if quantity > 0:
                new_basket_item.quantity = quantity
                new_basket_item.save()
            else:
                new_basket_item.delete()
            basket_items = Basket.objects.filter(user=request.user).order_by('product__name')
            context = {
                'basket': basket_items,
            }
            result = render_to_string('basketapp/includes/inc_basket_list.html', context)
            return JsonResponse({'result': result})
