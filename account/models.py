from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=7)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
