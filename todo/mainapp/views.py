from django.shortcuts import render
from mainapp.models import Project, ToDo, UserOnProject, Executor
from .serializers import ProjectModelSerializer, TodoModelSerializer, UserOnProjectSerializer, ExecutorToDoModelSerializer
from rest_framework.viewsets import ModelViewSet


# Create your views here.


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer


class ToDoViewSet(ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = TodoModelSerializer


class UserOnProjectViewSet(ModelViewSet):
    queryset = UserOnProject.objects.all()
    serializer_class = UserOnProjectSerializer


class ExecutorViewSet(ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorToDoModelSerializer
