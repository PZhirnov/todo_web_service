from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class ApiUser(AbstractUser):
    uid = models.UUIDField(primary_key=True, default=uuid4(), null=False)
    email = models.EmailField(unique=True)
    add_datetime = models.DateTimeField(verbose_name='дата и время создания', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='последнее изменение', auto_now=True)

# Create your models here.
