from django.db import models
from uuid import uuid4

# Create your models here.


class AppUsers(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4(), null=False, unique=True)
    username = models.CharField(verbose_name='логин пользователя',  max_length=64, unique=True, null=False)
    email = models.EmailField(verbose_name='email пользователя', null=False, unique=True)
    first_name = models.CharField(verbose_name='имя пользователя', max_length=64, null=False)
    last_name = models.CharField(verbose_name='фамилия пользователя', max_length=64, null=True)
    birthday = models.DateField(verbose_name='дата рождения пользоватя')
    is_active = models.BooleanField(verbose_name="активный пользователь", default=True)
    add_datetime = models.DateTimeField(verbose_name='дата и время создания', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='последнее изменение', auto_now=True)
