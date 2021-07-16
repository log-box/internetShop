from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ProductsCategoryCreateForm, ProductsCategoryEditForm
from mainapp.models import ProductCategory


def category_create(request):
    title = f'Создание категории продуктов'
    if request.method == 'POST':
        create_form = ProductsCategoryCreateForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:categories'))
    else:
        create_form = ProductsCategoryCreateForm()
    context = {
        'title': title,
        'create_form': create_form,
    }
    return render(request, 'adminapp/category_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'Админка/Категории'
    get_categories = ProductCategory.objects.all()

    context = {
        'title': title,
        'categories': get_categories,
    }
    return render(request, 'adminapp/categories.html', context)


def category_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    title = f'Редактировние {category.name}'
    if request.method == 'POST':
        edit_form = ProductsCategoryEditForm(request.POST, instance=category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:categories'))
    else:
        edit_form = ProductsCategoryEditForm(instance=category)
    context = {
        'title': title,
        'edit_form': edit_form,
    }
    return render(request, 'adminapp/category_update.html', context)


def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    title = f'Удаление {category.name}'
    if request.method == 'POST':
        category.is_deleted = True
        category.save()
        return HttpResponseRedirect(reverse('admin_stuff:categories'))
    context = {
        'title': title,
        'category': category,
    }
    return render(request, 'adminapp/category_delete.html', context)