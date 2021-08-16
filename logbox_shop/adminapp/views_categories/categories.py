from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from adminapp.forms import ProductsCategoryCreateForm, ProductsCategoryEditForm
from mainapp.models import ProductCategory


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_deleted:
            instance.product_set.update(is_deleted=True)
        else:
            instance.product_set.update(is_deleted=False)
    db_profile_by_type(sender, 'UPDATE', connection.queries)


class CategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductsCategoryCreateForm
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admin_stuff:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data()
        context['title'] = 'Создание категории продуктов'
        return context


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_stuff:categories')
    form_class = ProductsCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'категории/редактирование {self.object.name}'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_stuff:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление  {self.object.name}'
        return context
