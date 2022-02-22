from django.db import models
from uuid import uuid4
# Create your models here.


class User(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4(), unique=True)
    username = models.CharField(verbose_name='логин пользователя',  max_length=64, unique=True, null=False)
    email = models.EmailField(verbose_name='email пользователя', null=False, unique=True)
    first_name = models.CharField(verbose_name='имя пользователя', max_length=64, null=False)
    last_name = models.CharField(verbose_name='фамилия пользователя', max_length=64, null=True)
    birthday_year = models.PositiveIntegerField()
