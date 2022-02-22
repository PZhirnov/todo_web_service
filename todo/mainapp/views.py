from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from mainapp.models import AppUsers
from .serializers import AppUsersSerializer


class AppUserViewSet(ModelViewSet):
    queryset = AppUsers.objects.all()
    serializer_class = AppUsersSerializer
