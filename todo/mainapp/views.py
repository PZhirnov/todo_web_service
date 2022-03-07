from django.shortcuts import render
from mainapp.models import Project, ToDo, UserOnProject, Executor
from .serializers import ProjectModelSerializer, TodoModelSerializer, UserOnProjectSerializer, ExecutorToDoModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from mainapp.filters import ProjectFilter

# Create your views here.
# ●	модель Project: доступны все варианты запросов;
# для постраничного вывода установить размер страницы 10 записей; добавить фильтрацию по совпадению части названия проекта;


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    # filterset_fields = ['name']
    filterset_class = ProjectFilter
    pagination_class = ProjectLimitOffsetPagination


class ToDoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class ToDoViewSet(ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = TodoModelSerializer
    filterset_fields = ['project']
    pagination_class = ToDoLimitOffsetPagination

    # def perform_destroy(self, instance):
    #     super(ToDoViewSet, self).perform_destroy(instance)
    #     print(instance)
    #     instance.is_active = False
    #     instance.save()


class UserOnProjectViewSet(ModelViewSet):
    queryset = UserOnProject.objects.all()
    serializer_class = UserOnProjectSerializer


class ExecutorViewSet(ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorToDoModelSerializer
