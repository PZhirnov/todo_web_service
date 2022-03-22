from django.core.management.base import BaseCommand, CommandError
from authapp.models import User
from mainapp.models import Project, UserOnProject, ToDo, Executor
from random import random
from uuid import uuid4


def add_project(name, description, initiator, href_repo='n/a'):
    project = Project(name=name, description=description, initiator_project=initiator, href_repo=href_repo)
    project.save()
    return project


def add_user_on_project(project, user):
    user_on_project = UserOnProject(project_id=project.pk, user_id=user.pk)
    user_on_project.save()


def add_todo(project, title='n/a', description='n/a'):
    todo = ToDo(project_id=project, title=title, description=description)
    todo.save()
    return todo


def add_executor(todo, user):
    executor = Executor(todo=todo, user_on_project=user)
    executor.save()


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Добавим проект
        users = User.objects.all()
        for i in range(10):
            project = add_project(name=f'Новый проект {round(random()*1000)}', description='Замечательный проект',
                                  initiator=users[round(random() * (len(users)-1) + 1)-1])
            # Добавим пользователей на проекты
            for user in users[:round(random() * len(users))]:
                add_user_on_project(project, user)

            user_on_project = UserOnProject.objects.filter(project_id=project)
            print(user_on_project)
            # Добавим задачи (to_do) на проект и исполнителей - рандомно
            for i in range(int(random()*10)):
                todo = add_todo(project)
                add_executor(todo, user_on_project[round(random() * (len(user_on_project)-1)+1)-1])
