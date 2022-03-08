from django.http import Http404
from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from mainapp.models import Project, ToDo, UserOnProject, Executor
from .serializers import ProjectModelSerializer, TodoModelSerializer, UserOnProjectSerializer, ExecutorToDoModelSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import LimitOffsetPagination
from mainapp.filters import ProjectFilter

# Create your views here.

# п.3.2. Модель Project: доступны все варианты запросов;
# для постраничного вывода установить размер страницы 10 записей; добавить фильтрацию по совпадению части названия проекта;


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    # filterset_fields = ['name']
    filterset_class = ProjectFilter
    pagination_class = ProjectLimitOffsetPagination


# п.3.3.
# ToDo: доступны все варианты запросов; при удалении не удалять ToDo,
#  а выставлять признак, что оно закрыто; добавить фильтрацию по проекту;
#  для постраничного вывода установить размер страницы 20.

class ToDoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class ToDoViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = ToDo.objects.all()
    serializer_class = TodoModelSerializer
    filterset_fields = ['project']
    pagination_class = ToDoLimitOffsetPagination
    # http_method_names = ['get', 'post', 'head', 'delete']

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
