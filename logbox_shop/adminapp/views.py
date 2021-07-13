from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ShopUserAdminRegisterForm, ProductsCategoryEditForm, \
    ProductsCategoryCreateForm, ProductEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


def user_create(request):
    title = f'Создание пользователя'
    if request.method == 'POST':
        create_form = ShopUserAdminRegisterForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:users'))
    else:
        create_form = ShopUserAdminRegisterForm()
    context = {
        'title': title,
        'form': create_form,
    }
    return render(request, 'adminapp/user_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'Админка/Пользователи'
    get_users = ShopUser.objects.all()

    context = {
        'title': title,
        'users': get_users,
    }
    return render(request, 'adminapp/users.html', context)


def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    title = f'Редактировние {user.username}'
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:users'))
    else:
        edit_form = ShopUserAdminEditForm(instance=user)
    context = {
        'title': title,
        'edit_form': edit_form,
    }
    return render(request, 'adminapp/user_update.html', context)


def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    title = f'Удаление {user.username}'
    if request.method == 'POST':
        user.is_deleted = True
        user.save()
        return HttpResponseRedirect(reverse('admin_stuff:users'))
    context = {
        'title': title,
        'user': user,
    }
    return render(request, 'adminapp/user_delete.html', context)


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


def product_create(request, pk):
    title = f'Создание нового продукта'
    product = Product.objects.filter(category_id=pk)[0]
    if request.method == 'POST':
        create_form = ProductEditForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:products', kwargs={'pk': product.category.pk}))
    else:
        create_form = ProductEditForm()
    context = {
        'title': title,
        'create_form': create_form,
        'product': product,
    }
    return render(request, 'adminapp/product_create.html', context)


def products(request, pk):
    products = Product.objects.filter(category_id=pk)
    one_product = Product.objects.filter(category_id=pk)[0]

    title = f'Товары категории "{one_product.category}"'
    context = {
        'title': title,
        'products': products,
        'prod': one_product,
    }
    return render(request, 'adminapp/products.html', context)


def product_read(request):
    pass


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'Редактировние {product.name}'
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, instance=product)
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
