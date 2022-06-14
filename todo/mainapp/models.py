from django.db import models
from uuid import uuid4
from authapp.models import User

# Create your models here.
# uid пока отключил, чтобы было проще добавлять данные при тесте
# В промежуточной таблице будут хранить данные о даты выдаче задания, поэтому в моделях
# данные таблицы были созданы вручную


# Projects
class Project(models.Model):
    # uid = models.UUIDField(verbose_name='id проекта', primary_key=True, default=uuid4())
    name = models.CharField(verbose_name='наименование проекта', max_length=64, blank=False, unique=True)
    description = models.TextField(verbose_name='описание проекта')
    href_repo = models.URLField(verbose_name='ccылка на репозиторий')
    # initiator_project = models.ForeignKey(User, on_delete=models.SET('n/a'), verbose_name='uid инициатор проекта')
    user_on_project = models.ManyToManyField(User, verbose_name='пользователь на проекте', through='UserOnProject')
    add_date = models.DateTimeField(verbose_name='дата добавления проекта в БД', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='дата последнего изменния', auto_now=True)

    def __str__(self):
        return self.name


# Executor on Project
# В данной модели храним всех пользователей, которые были выделены на проект
class UserOnProject(models.Model):
    # uid = models.UUIDField(verbose_name='id связи c исполнителем', primary_key=True, default=uuid4())
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    add_date = models.DateTimeField(verbose_name='дата добавления проекта в БД', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='дата последнего изменния', auto_now=True)

    def __str__(self):
        return f"{self.project} "

    def get_user(self):
        return self.user


# Описание полей заметки
class ToDo(models.Model):
    # uid = models.UUIDField(verbose_name='id заметки', primary_key=True, default=uuid4())

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_on_todo = models.ManyToManyField(UserOnProject, through='Executor')

    title = models.CharField(verbose_name='заголовок заметки', max_length=64,
                             unique=False, default='не определен')
    description = models.TextField(verbose_name='текст заметки', default='не определен')
    is_active = models.BooleanField(verbose_name='статус заметки', default=True)
    is_close = models.BooleanField(verbose_name='закрыто', default=False)
    scheduled_date = models.DateTimeField(verbose_name='плановая дата завершения', null=True)
    actual_date = models.DateTimeField(verbose_name='фактическая дата завершения', null=True)
    add_date = models.DateTimeField(verbose_name='дата добавления проекта в БД', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='дата последнего изменния', auto_now=True)

    def __str__(self):
        return f"{self.project_id} - {self.title}"


# Исполнитель заметки - user
class Executor(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    user_on_project = models.ForeignKey(UserOnProject, on_delete=models.SET_NULL, null=True)
    add_date = models.DateTimeField(verbose_name='дата добавления проекта в БД', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='дата последнего изменния', auto_now=True)
