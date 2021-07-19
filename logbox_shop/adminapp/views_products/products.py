from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

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
        context['title'] = f'Товары категории "{ProductCategory.objects.filter(id=self.kwargs.get("pk"))}"' # ДОДЕЛАТЬ!!!!!!!! prod.0.category
        context['object_list'] = Product.objects.filter(category_id=self.kwargs.get('pk'))
        context['prod'] = get_pk(self)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = f'продукт/{self.object.name}'
        return content


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = 'admin_stuff:products'
    form_class = ProductEditForm

    def get_success_url(self):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return reverse_lazy('admin_stuff:products', kwargs={'pk': product.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактировние {self.object.name}'
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = 'admin_stuff:products'

    def get_success_url(self):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return reverse_lazy('admin_stuff:products', kwargs={'pk': product.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление {self.object.name}'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


