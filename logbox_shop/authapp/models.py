from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True,
    )

    age = models.PositiveIntegerField(
        verbose_name='возраст',
        null=True,
        blank=True,
    )

    email = models.EmailField(
        verbose_name='почта',
        unique=True,
    )

    is_deleted = models.BooleanField(default=False)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=now() + timedelta(hours=48))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOISE = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(
        ShopUser,
        unique=True,
        blank=False,
        db_index=True,
        on_delete=models.CASCADE,
    )

    tagline = models.CharField(
        verbose_name='теги',
        max_length=128,
        blank=True,
    )

    about_me = models.TextField(
        verbose_name='о себе',
        max_length=512,
        blank=True,
    )

    gender = models.CharField(
        verbose_name='',
        max_length=1,
        choices=GENDER_CHOISE,
        blank=True,
    )

    @receiver(post_save, sender=ShopUser)
    def create_user_profiler(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profiler(sender, instance, **kwargs):
        instance.shopuserprofile.save()
        