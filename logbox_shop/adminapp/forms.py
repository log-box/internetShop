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
        fields = ['name', 'description', 'href', 'is_deleted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = ''
            field.help_text = ''

    @staticmethod
    def check_for_russian(string):
        alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
                    "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
        for one_char in string:
            if one_char.lower() in alphabet:
                return False
        return True

    @staticmethod
    def check_for_symbols(string):
        symbols = ["_", "-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        for one_char in string:
            if one_char in symbols:
                return True
        return False

    def clean_href(self):
        href = self.cleaned_data['href']
        if href == '':
            raise forms.ValidationError("Ссылка обязательно нужна")
        if self.check_for_russian(href) == False or self.check_for_symbols(href) == False:
            raise forms.ValidationError('Допускаются только латинские символы и знаки ("_" "-") и цифры "0-9"')
        return href


class ProductsCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'href', 'is_deleted']

    @staticmethod
    def check_for_russian(string):
        alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
                    "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
        for one_char in string:
            if one_char.lower() in alphabet:
                return False
        return True

    @staticmethod
    def check_for_symbols(string):
        symbols = ["_", "-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        for one_char in string:
            if one_char in symbols:
                return True
        return False

    def clean_href(self):
        href = self.cleaned_data['href']
        if href == '':
            raise forms.ValidationError("Ссылка обязательно нужна")
        if self.check_for_russian(href) == False or self.check_for_symbols(href) == False:
            raise forms.ValidationError('Допускаются только латинские символы и знаки ("_" "-") и цифры "0-9"')
        return href


class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

