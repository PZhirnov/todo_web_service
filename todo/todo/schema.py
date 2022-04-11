"""
    Задача:
    Необходимо с помощью GraphQl создать схему, которая позволит одновременно получить ToDo, проекты и пользователей, связанных с проектом
"""

import graphene
from graphene_django import DjangoObjectType
from mainapp.models import Project, ToDo, UserOnProject, Executor
from authapp.models import User


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class ToDoType(DjangoObjectType):
    class Meta:
        model = ToDo
        fields = '__all__'


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class UserOnProjectType(DjangoObjectType):
    class Meta:
        model = UserOnProject
        fields = '__all__'


class ExecutorType(DjangoObjectType):
    class Meta:
        model = Executor
        fields = '__all__'


class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    all_todo = graphene.List(ToDoType)
    all_user = graphene.List(UserType)
    user_on_project = graphene.List(UserOnProjectType)

    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_all_todo(root, info):
        return ToDo.objects.all()

    def resolve_all_user(root, info):
        return User.objects.all()

    def resolve_user_on_project(root, info):
        return UserOnProject.objects.all()

    def resolve_executor(root, info):
        return Executor.objects.all()


schema = graphene.Schema(query=Query)


"""
------- ЗАПРОСЫ ПО ВСЕМ ДАННЫМ В БД -------
----- 1. Все проекты

{
  allProjects {
    id
    name
  }
}

----- 2. Все проекты c задачами

{
  allProjects {
    id
    name
    todoSet {
      id
      title
    }
  }
}

----- 3. Пользователи на проекте

{
  allProjects {
    id
    name
    hrefRepo
    useronprojectSet {
      id
      user {
        username
        addDatetime
        lastModified
      }
    }
  }
}

----- 4. Детализация задач на проекте и исполнители

{
  allProjects {
    id
    name
    todoSet {
      id
      title
      description
      isActive
      isClose
      addDate
      lastModified
      executorSet {
        userOnProject {
          user {
            id
            username
          }
        }
      }
    }
  }
}

5. Все проекты и задачи по пользователям
{
  allUser {
    id
    username
    projectSet {
      id
      name
      todoSet {
        id
        title
        description
      }
    }
  }
}
"""

