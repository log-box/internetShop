from django.conf import settings

from authapp.models import ShopUser


def test_user_register(self):
    # логин без данных пользователя
    response = self.client.get('/auth/register/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['title'], 'регистрация')
    self.assertTrue(response.context['user'].is_anonymous)

    new_user_data = {
        'username': 'samuel',
        'first_name': 'Сэмюэл',
        'last_name': 'Джексон',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'email': 'sumuel@geekshop.local',
        'age': '21'}

    response = self.client.post('/auth/register/', data=new_user_data)
    self.assertEqual(response.status_code, 302)

    new_user = ShopUser.objects.get(username=new_user_data['username'])

    activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"

    response = self.client.get(activation_url)
    self.assertEqual(response.status_code, 200)

    # данные нового пользователя
    self.client.login(username=new_user_data['username'], \
                      password=new_user_data['password1'])

    # логинимся
    response = self.client.get('/auth/login/')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.context['user'].is_anonymous)

    # проверяем главную страницу
    response = self.client.get('/')
    self.assertContains(response, text=new_user_data['first_name'], \
                        status_code=200)


def test_user_wrong_register(self):
    new_user_data = {
        'username': 'teen',
        'first_name': 'Мэри',
        'last_name': 'Поппинс',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'email': 'merypoppins@geekshop.local',
        'age': '17'}

    response = self.client.post('/auth/register/', data=new_user_data)
    self.assertEqual(response.status_code, 200)
    self.assertFormError(response, 'register_form', 'age', \
                         'Вы слишком молоды!')
