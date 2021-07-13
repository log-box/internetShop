from django import forms
from django.forms import ModelForm

from authapp.forms import ShopUserEditForm, ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-group'
            field.help_text = ''


class ShopUserAdminRegisterForm(ShopUserRegisterForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-group'
            field.help_text = ''


class ProductsCategoryEditForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'is_deleted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = ''
            field.help_text = ''


class ProductsCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'is_deleted']


class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = ''
    #         field.help_text = ''


