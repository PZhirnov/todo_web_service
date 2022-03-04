from django.shortcuts import render
from mainapp.models import Project, ToDo
from .serializers import ProjectModelSerializer, TodoModelSerializer
from rest_framework.viewsets import ModelViewSet


# Create your views here.


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer


class ToDoViewSet(ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = TodoModelSerializer








