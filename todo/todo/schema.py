"""
    Задача:
    Необходимо с помощью GraphQl создать схему, которая позволит одновременно получить ToDo, проекты и пользователей, связанных с проектом
"""

import graphene
from graphene_django import DjangoObjectType
from mainapp.models import Project, ToDo, UserOnProject, Executor
from authapp.models import User
from datetime import datetime
from django.db.models import Q


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
    # Получить данне о проекте по имени или id
    project_by_id_or_name = graphene.Field(ProjectType, id=graphene.Int(required=True),
                                           name=graphene.String(required=True))
    project_by_name_contains = graphene.List(ProjectType, name=graphene.String(required=True))
    # Добавил поле, которое возвращает дату запроса
    query_datetime = graphene.String(default_value=datetime.now())
    # Поиск сотрудника по имени или фамилии
    search_user = graphene.List(UserType, search_text=graphene.String(required=True))

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

    def resolve_project_by_id_or_name(self, info, id=None, name=None):
        """
            Получаем проект по id или по полному имени, если указано
        """
        try:
            # если в запросе id > 0, то выводим данные
            if id > 0:
                return Project.objects.get(id=id)
            elif name:
                return Project.objects.get(name=name)
        except Project.DoesNotExist:
            return None

    def resolve_project_by_name_contains(self, info, name=None):
        return Project.objects.filter(name__contains=name) if name else None

    def resolve_search_user(self, info, search_text):
        """
            выводим всех сотрудников, имя или фамилия которых содержит search_text
        """
        return User.objects.filter(Q(username__contains=search_text)
                                   | Q(first_name__contains=search_text)
                                   | Q(last_name__contains=search_text))



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


6. Получение данных по проекту по его id или полному имени
{
  projectByIdOrName(id: 0, name: "Новый проект 476") {
    id
    name
    description
    addDate
    lastModified
  }
  queryDatetime
}

7. Поиск проекта по части наименования

{
  projectByNameContains(name: "23") {
    id
    name
    description
    addDate
    lastModified
  }
  queryDatetime
}

8. Поиск пользователя по части имени, фаилии или имени пользователя
{
  searchUser(searchText: "Pa") {
    id
    username
    firstName
    lastName
  }
}

9. Вывод списка проектов и задач по имени / части имени пользователя
{
  searchUser(searchText: "Pa") {
    id
    username
    firstName
    lastName
    projectSet{
      id
      name
      todoSet{
        id
        title
      }
    }
  }
  
}



"""

