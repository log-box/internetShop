from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ShopUserAdminRegisterForm
from authapp.models import ShopUser


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
        # user_pk = request.POST.get('target_user_pk')
        # user = get_object_or_404(ShopUser, pk=user_pk)
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:users'))
    else:
        edit_form = ShopUserAdminEditForm(instance=user)
    context = {
        'title': title,
        'edit_form': edit_form,
        # 'target_user_pk': pk,
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
    pass


def categories(request):
    pass


def category_update(request):
    pass


def category_delete(request):
    pass


def product_create(request):
    pass


def products(request):
    pass


def product_read(request):
    pass


def product_update(request):
    pass


def product_delete(request):
    pass
