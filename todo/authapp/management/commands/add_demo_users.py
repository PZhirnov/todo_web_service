from django.core.management.base import BaseCommand, CommandError
from authapp.models import User
from uuid import uuid4


def create_user(username, password, email="", firstName="", lastName="", is_superuser=False):
    """
    Функция создает суперпользователя
    """
    try:
        user = User(username=username, email=email, first_name=firstName, last_name=lastName)
        user.set_password(password)
        # user.uid = uuid4()
        user.is_superuser = is_superuser
        user.is_staff = False
        user.save()
        return user
    except Exception as exc:
        print('Суперпользователь ранее был создан / или не уникальный.', exc)


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # super_user = ApiUser.objects.create_superuser('django2', 'django@new.ru', 'geekbrains')
        create_user('django', 'geekbrains', 'django@geek.ru', 'Django', 'Admin', is_superuser=True)
        create_user('Alice', 'geekbrains', 'alisa@geek.ru', 'Alisa', 'Liddel')
        create_user('Mary', 'geekbrains', 'mary@geek.ru', 'Mary', 'Poppins')
        create_user('Pavel', 'geekbrains', 'pavel@geek.ru', 'Pavel', 'Zhirnov')
        create_user('Fedor', 'geekbrains', 'fedor@geek.ru', 'Fedor', 'Nikonov')
        create_user('Evgenyi', 'geekbrains', 'evg@geek.ru', 'Evgeniy', 'Sam')
