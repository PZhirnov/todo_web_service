# from django.http import Http404
# from django.shortcuts import render
from rest_framework import mixins, status, permissions
# from rest_framework.decorators import action
# from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Project, ToDo, UserOnProject, Executor
from .serializers import ProjectModelSerializer, ProjectSerializerBase,\
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
    # serializer_class = ProjectModelSerializer
    # filterset_fields = ['name']
    filterset_class = ProjectFilter
    pagination_class = ProjectLimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        '''
           ProjectSerializerBase используется для сохранения/обновления данных
        '''
        if self.request.method in ['GET']:
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


class ToDoViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = ToDo.objects.all()
    # serializer_class = TodoModelSerializer
    filterset_fields = ['project_id']
    pagination_class = ToDoLimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]
    # http_method_names = ['get', 'post', 'head', 'delete']

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


class ExecutorViewSet(ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorToDoModelSerializer


class SwaggerTemplateView(TemplateView):
    template_name = 'swagger-ui.html'
    extra_context = {'schema_url': 'openapi-schema'}


class RedocTemplateView(TemplateView):
    template_name = 'redoc.html'
    extra_context = {'schema_url': 'openapi-schema'}
