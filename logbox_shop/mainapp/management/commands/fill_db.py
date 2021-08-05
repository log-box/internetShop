import json
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

JSON_DIR = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_DIR, file_name + '.json'), mode='r', encoding='UTF-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        for product in products:
            product['category'] = ProductCategory.objects.get(name=product['category'])
            new_product = Product(**product)
            new_product.save()

        ShopUser.objects.create_superuser(username='admin', password='admin', age=37)
