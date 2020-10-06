from django.db import models
from django.contrib.auth.models import User
from account.models import *


def get_upload_path(instance, filename):
    return 'product-' + str(instance.id) + '/' + filename


class ProductPermanent(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    description = models.CharField(max_length=500)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to=get_upload_path, default='settings.MEDIA_ROOT/product_default.png')


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    description = models.CharField(max_length=500)
    stock = models.IntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to=get_upload_path, default='product_default.png')
    product_permanent = models.OneToOneField(ProductPermanent, on_delete=models.SET_NULL, null=True, default=None)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='InCart')


class InCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(ProductPermanent, through='InOrder')
    total_price = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.CharField(choices=[('C', 'Confirmed'),
                                       ('S', 'Shipped'),
                                       ('D', 'Delivered')],
                              max_length=10,
                              default='C')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)


class InOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductPermanent, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
