from django.db import models
import json


# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='категория',
        max_length=64,
        unique=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    href = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name or f'Category with id - {self.pk}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        # on_delete=models.DO_NOTHING,
        verbose_name='категория',
    )
    name = models.CharField(
        verbose_name='имя товара',
        max_length=128,
    )
    image = models.ImageField(
        upload_to='products_images',
        blank=True,
        verbose_name='Изображение товара',
    )
    short_desc = models.CharField(
        verbose_name='краткое описание',
        max_length=100,
    )

    description = models.TextField(
        verbose_name='описание товара',
        blank=True,
    )

    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    quantity = models.PositiveIntegerField(
        verbose_name='количество товара на складе',
        default=0,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name or f'Product with id - {self.pk}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукция'
