from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView, CreateView

from adminapp.forms import ShopUserAdminRegisterForm
from authapp.models import ShopUser


class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserAdminRegisterForm
    template_name = 'adminapp/user_create.html'
    success_url = reverse_lazy('admin_stuff:users')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'Создание пользователя'
        return context


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_stuff:users')
    fields = ('username', 'first_name', 'email', 'age', 'avatar', 'is_deleted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование пользователя ' + str(ShopUser.objects.get(username=self.request.user.username))
        return context


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