from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


from mainapp.models import ProductCategory, Product
from adminapp.forms import ProductEditForm


def product_create(request, pk):
    title = f'Создание нового продукта'
    product = Product.objects.filter(category_id=pk)[0]
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        create_form = ProductEditForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:products', kwargs={'pk': product.category.pk}))
    else:
        create_form = ProductEditForm(initial={'category': category})
    context = {
        'title': title,
        'create_form': create_form,
        'product': product,
    }
    return render(request, 'adminapp/product_create.html', context)


def products(request, pk):
    products = Product.objects.filter(category_id=pk)
    if len(products) > 0:
        one_product = Product.objects.filter(category_id=pk)[0]
        title = f'Товары категории "{one_product.category}"'
    else:
        one_product = Product.objects.first()
        title = 'Пустая категория'

    context = {
        'title': title,
        'products': products,
        'prod': one_product,
    }
    return render(request, 'adminapp/products.html', context)


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