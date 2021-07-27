from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser
from logbox_shop import settings



def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Активация пользователя {user.username}'

    message = f'Для активации учетной записи {user.email} на сайте {settings.DOMAIN_NAME}' \
              f'перейдите по ссылке \n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            err = f'error activation user {user.username}. Истек срок активации или ссылка была скоппроментирована' \
                  f'повторите регистрацию'
            print(f'error activation user {user.username}')
            context = {
                'err': err,
            }
            user.delete()
            return render(request, 'authapp/verification.html', context)
    except Exception as err:
        print(f'error activation user: {err.args}')
        return HttpResponseRedirect(reverse('index'))


class ShopLoginView(LoginView):
    template_name = 'authapp/login.html'
    authentication_form = ShopUserLoginForm

    def get_success_url(self):
        if 'next' in self.request.POST.keys():
            return resolve_url(self.request.POST['next'])
        else:
            return reverse_lazy('index')


class ShopLogoutView(LogoutView):
    template_name = None


class ShopRegisterView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        context = super(ShopRegisterView, self).get_context_data()
        context['title'] = 'Регистрация нового пользователя'
        return context

    def post(self, request, **kwargs):
        self.object = ShopUser()
        form = super().get_form(self.form_class)
        if form.is_valid():
            user = form.save()
            if send_verify_email(user):
                print('Письмо отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('Письмо не отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            return self.form_invalid(form)


class ShopUpdateView(UpdateView):
    template_name = 'authapp/edit.html'
    success_url = reverse_lazy('auth:edit')

    form_class = ShopUserEditForm
    profile_form_class = ShopUserProfileEditForm

    @transaction.atomic
    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = super().get_form(self.form_class)
        form2 = self.profile_form_class(request.POST, instance=self.object.shopuserprofile)
        if form.is_valid() and form2.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование пользователя {self.object.username}'
        context['form2'] = self.profile_form_class(instance=self.object.shopuserprofile)
        return context

    def get_object(self, queryset=None):
        return self.request.user

