from django.shortcuts import render

# Create your views here.
from authapp.models import ShopUser


def user_create(request):
    pass


def users(request):
    title = 'Админка/Пользователи'
    get_users = ShopUser.objects.all()

    context = {
        'title': title,
        'users': get_users,
    }
    return render(request, 'adminapp/users.html', context)


def user_update(request):
    pass


def user_delete(request):
    pass


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
