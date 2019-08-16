import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.admin import models as Log
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django_resized import ResizedImageField

from main.helpers import path_and_rename_product, delete_image_file


class User(AbstractUser):
    deleted_in = models.DateField(auto_now=False, auto_now_add=False,
                                  null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)

    @property
    def profile(self):
        if self.is_superuser:
            return "superuser"
        if hasattr(self, "client"):
            return "client"
        return None


class LogSystem(Log.LogEntry):
    date_register = models.DateField(auto_now=False, auto_now_add=True)


class Client(models.Model):

    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    cpf = models.CharField(max_length=11, unique=True, blank=False, null=False)
    birthday = models.DateField(auto_now=False, auto_now_add=False,
                                blank=True, null=True)
    gender = models.CharField(max_length=2, choices=CHOICES, blank=False,
                              null=False)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        default=None
    )


class Brand(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    deleted_in = models.DateField(auto_now=False, auto_now_add=False,
                                  null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return '%s' % (self.name)


class ExtraProductType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    value = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    deleted_in = models.DateField(auto_now=False, auto_now_add=False,
                                  null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return '(cod): %s, (description): %s - %s' % (self.name, self.description, self.value)


class ProductType(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    description = models.CharField(max_length=50, blank=True, null=True, unique=True)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    deleted_in = models.DateField(auto_now=False, auto_now_add=False,
                                  null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return '%s' % (self.description)


class Product(models.Model):
    code_name = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    typeproduct = models.ForeignKey(ProductType,
                                    on_delete=models.SET_NULL,
                                    related_name='product',
                                    blank=True,
                                    null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    brand = models.ForeignKey(Brand,
                              on_delete=models.SET_NULL,
                              related_name='brand',
                              blank=True,
                              null=True)
    image = ResizedImageField(
        size=[500, 300], upload_to=path_and_rename_product,
        null=True, blank=True)
    extra_product_type = models.ManyToManyField(ExtraProductType,
                              related_name='product_extra_type_list',
                              blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    deleted_in = models.DateField(auto_now=False, auto_now_add=False,
                                  null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return '%s - %s' % (self.name, self.typeproduct)


@receiver(pre_delete, sender=Product, dispatch_uid='product_delete_signal')
def product_delete(sender, instance, using, **kwargs):
    delete_image_file(instance)


class Request(models.Model):
    products = models.ManyToManyField(Product,
                              related_name='products_request',
                              blank=True)
    client = models.ForeignKey(Client,
                              on_delete=models.SET_NULL,
                              related_name='client_request',
                              blank=True,
                              null=True)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    deleted_in = models.DateField(auto_now=False, auto_now_add=False,
                                  null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)