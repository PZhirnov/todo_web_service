# from django.http import Http404
# from django.shortcuts import render
from rest_framework import mixins, status, permissions
# from rest_framework.decorators import action
# from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Project, ToDo, UserOnProject, Executor, User
from .serializers import ProjectModelSerializer, ProjectSerializerBase, \
    TodoModelSerializer, UserOnProjectSerializer, ExecutorToDoModelSerializer, TodoModelSerializerBase
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import LimitOffsetPagination
from mainapp.filters import ProjectFilter
from datetime import datetime, timedelta
from django.views.generic import TemplateView


# Create your views here.

# п.3.2. Модель Project: доступны все варианты запросов;
# для постраничного вывода установить размер страницы 10 записей;
# добавить фильтрацию по совпадению части названия проекта;


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100


class ProjectViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer]
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    filterset_fields = ['name']
    filterset_class = ProjectFilter
    # pagination_class = ProjectLimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        new_response = super(ProjectViewSet, self).create(request, *args, **kwargs)
        project = Project.objects.get(id=new_response.data['id'])
        users_id_on_project = request.data['user_on_project']
        if users_id_on_project:
            for user_id in users_id_on_project:
                user = User.objects.get(id=user_id['id'])
                project.user_on_project.add(user)
        project_serializer = ProjectModelSerializer(project)
        new_response.data = project_serializer.data
        print(project_serializer.data)
        return new_response

    def update(self, request, *args, **kwargs):
        new_response = super(ProjectViewSet, self).update(request, *args, **kwargs)
        print(new_response)

        # Получили проект по его id
        project = Project.objects.get(id=new_response.data['id'])

        # Получили пользователей, которые были добавлены на проект ранее
        user_on_project_from_bd = UserOnProject.objects.filter(project_id=project.id)

        # Список id пользователей, которые уже есть в базе
        print(user_on_project_from_bd.values('id', 'user_id'))
        users_id_on_project_bd = list(map(lambda x: x['user_id'],
                                           user_on_project_from_bd.values('id', 'user_id')))

        # Список пользователей из запроса на обновление
        print(request.data['user_on_project'])
        users_id_from_request = list(map(lambda x: int(x['id']), request.data['user_on_project']))

        # Удалили пользователей из БД, которые были удалены пользователем с проекта
        users_id_list_for_delete = list(set(users_id_on_project_bd) - set(users_id_from_request))
        user_on_project_from_bd.filter(user_id__in=users_id_list_for_delete).delete()

        # Добавили на проект пользователей из запроса, которые ранее не были на него запланированы
        users_id_list_for_add = list(set(users_id_from_request) - set(users_id_on_project_bd))
        users = User.objects.filter(id__in=users_id_list_for_add)
        project.user_on_project.add(*users)

        # Завершаем работу с данными и возвращаем ответ
        project_serializer = ProjectModelSerializer(project)
        new_response.data = project_serializer.data
        print(project_serializer.data)
        return new_response

    def get_serializer_class(self):
        '''
           ProjectSerializerBase используется для сохранения/обновления данных
        '''
        # print(self.request.data)
        print(self.request.method)
        if self.request.method == 'GET':
            return ProjectModelSerializer
        return ProjectSerializerBase


# п.3.3.
# ToDo: доступны все варианты запросов; при удалении не удалять ToDo,
#  а выставлять признак, что оно закрыто; добавить фильтрацию по проекту;
#  для постраничного вывода установить размер страницы 20.

class ToDoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100


def get_datetime(data_string: str, add_days=0):
    """
    Функция преобразует дату из текстового формата в формат datetime
    """
    try:
        data_string = data_string.replace('.', '/')
        date_time = datetime.strptime(data_string, "%d/%m/%Y")
        date_time += timedelta(days=add_days)
        return date_time
    except Exception as exc:
        return None


class ToDoViewSetBase(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = ToDo.objects.all()
    serializer_class = TodoModelSerializer


class ToDoViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer]
    queryset = ToDo.objects.all()
    # serializer_class = TodoModelSerializer
    filterset_fields = ['project_id']
    pagination_class = ToDoLimitOffsetPagination

    # permission_classes = [permissions.IsAuthenticated]
    # http_method_names = ['get', 'post', 'head', 'delete']

    def create(self, request, *args, **kwargs):
        new_response = super(ToDoViewSet, self).create(request, *args, **kwargs)
        print(request.data)
        print(new_response.data)
        # project = Project.objects.get(id=new_response.data['project_id'])
        new_todo = ToDo.objects.get(id=new_response.data['id'])
        users_on_todo_id_list = list(map(lambda i: int(i['id']), request.data['user_on_todo']))
        new_todo.user_on_todo.add(*users_on_todo_id_list)
        todo_serializer = TodoModelSerializer(new_todo)
        new_response.data = todo_serializer.data
        return new_response

    def update(self, request, *args, **kwargs):
        new_response = super(ToDoViewSet, self).update(request, *args, **kwargs)
        print(new_response.data)
        return new_response


    def get_serializer_class(self):
        '''
           Base используется для сохранения/обновления данных
        '''
        if self.request.method in ['GET']:
            return TodoModelSerializer
        return TodoModelSerializerBase

    def get_queryset(self):
        super(ToDoViewSet, self).get_queryset()
        # п.4  Фильтрация по дате создания - т.е. указываем интервал от и до, а после выбираем все попавшие записи
        # Пример запроса: http://127.0.0.1:8000/api/todo/?dateend=07.03.2022&datestart=07.03.2022
        date_start_param = self.request.query_params.get('datestart')
        date_end_param = self.request.query_params.get('dateend')
        if date_start_param and date_end_param:
            date_start_param = get_datetime(date_start_param)
            date_end_param = get_datetime(date_end_param, 1)
            self.queryset = ToDo.objects.filter(add_date__gte=date_start_param, add_date__lte=date_end_param)
        return self.queryset

    # После удаления выведем результат изменений в базе данных
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        serializer = self.get_serializer(instance)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # При удалении сделаем присвоим is_active False и сохраним данные
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.is_close = True
        instance.save()
        serializer = self.get_serializer(instance)
        # print(serializer.data)
        return Response(serializer.data)


class UserOnProjectViewSet(ModelViewSet):
    queryset = UserOnProject.objects.all()
    serializer_class = UserOnProjectSerializer


class UserOnProjectById(ModelViewSet):
    # queryset = UserOnProject.objects.all()
    serializer_class = UserOnProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        print(self.request.query_params)
        project_id = int(self.request.query_params['project_id'])
        print(project_id)
        users_on_project = UserOnProject.objects.filter(project_id=project_id)
        print(users_on_project)
        return users_on_project


class ExecutorViewSet(ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorToDoModelSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]


class SwaggerTemplateView(TemplateView):
    template_name = 'swagger-ui.html'
    extra_context = {'schema_url': 'openapi-schema'}


class RedocTemplateView(TemplateView):
    template_name = 'redoc.html'
    extra_context = {'schema_url': 'openapi-schema'}
