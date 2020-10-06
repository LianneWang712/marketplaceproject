from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ChatRoom(models.Model):
    members = models.ManyToManyField(User, through='InRoom')
    chat_log = models.TextField(default='')


class InRoom(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
