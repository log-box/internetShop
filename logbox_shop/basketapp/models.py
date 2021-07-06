from django.db import models
from django.db.models import Sum
# Create your models here.
from django.db.models import Sum

from logbox_shop import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )
    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True,
    )


    # @property
    def get_sum(self):
        return self.quantity*self.product.price
    # def total_sum(request):
    #     total_sum = Basket.objects.filter(user__id=request.user).aggregate(Sum('product__price'))
    #     return total_sum
    total_sum = property(get_sum)