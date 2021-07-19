from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from adminapp.forms import ProductEditForm
from mainapp.models import ProductCategory, Product


# вычисляю pk товара, для формирования обратных адресов на текущую категорию товара
def get_pk(self):
    if len(Product.objects.filter(category_id=self.kwargs.get('pk'))) > 0:
        return Product.objects.filter(category_id=self.kwargs.get('pk'))
    else:
        return {'category': ProductCategory.objects.get(id=self.kwargs.get("pk")),
                'pk': ProductCategory.objects.get(id=self.kwargs.get("pk")).pk},
###################################################################################


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_create.html'
    success_url = reverse_lazy('admin_stuff:products')

    def get_success_url(self):
        return reverse_lazy('admin_stuff:products',
                            kwargs={'pk': ProductCategory.objects.get(id=self.kwargs.get("pk")).pk})

    def get_initial(self):
        initial = super(ProductCreateView, self).get_initial()
        initial['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        initial['price'] = ''
        initial['quantity'] = ''
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание нового продукта'
        context['product'] = get_pk(self)
        return context


class ProductsCreateView(CreateView):
    model = Product
    template_name = 'adminapp/products.html'
    form_class = ProductEditForm
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Товары категории "{ProductCategory.objects.filter(id=self.kwargs.get("pk"))}"'
        context['object_list'] = Product.objects.filter(category_id=self.kwargs.get('pk'))
        context['prod'] = get_pk(self)
        return context


def product_read(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'продукт/{product.name}'
    context = {
        'title': title,
        'product': product,
    }
    return render(request, 'adminapp/product_read.html', context)


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'Редактировние {product.name}'
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:products', kwargs={'pk': product.category.pk}))
    else:
        edit_form = ProductEditForm(instance=product)
    context = {
        'title': title,
        'edit_form': edit_form,
        'product': product,
    }
    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'Удаление {product.name}'
    if request.method == 'POST':
        product.is_deleted = True
        product.save()
        return HttpResponseRedirect(reverse('admin_stuff:products', kwargs={'pk': product.category.pk}))
    context = {
        'title': title,
        'product': product,
    }
    return render(request, 'adminapp/product_delete.html', context)
