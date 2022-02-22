from django.core.management.base import BaseCommand, CommandError
from mainapp.models import AppUsers
from django.contrib.auth.models import User
from mainapp.models import AppUsers
from datetime import datetime, timedelta
from uuid import uuid4


def create_super_user(username, password, email="", firstName="", lastName=""):
    """
    Функция создает суперпользователя
    """
    try:
        user = User(username=username, email=email, first_name=firstName, last_name=lastName)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    except Exception as exc:
        print('Суперпользователь ранее был создан / или не уникальный.')


def create_user_app(username, password, email="", firstName="", lastName="", birthday=""):
    """
    Функция создает пользователя приложения
    """
    try:
        user = AppUsers(username=username, email=email, first_name=firstName, last_name=lastName)
        user.uid = uuid4()
        user.is_active = True
        user.birthday = datetime(1990, 10, 2)
        user.save()
        return user
    except Exception:
        print(f'Пользователь ранее был создан / или не уникальный.')


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        create_super_user('django', 'geekbrains', 'django@geek.ru', 'Django', 'Admin')
        create_user_app('Alice', 'geekbrains', 'alisa@geek.ru', 'Alisa', 'Liddel')
        create_user_app('Mary', 'geekbrains', 'mary@geek.ru', 'Mary', 'Poppins')
