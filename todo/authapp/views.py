from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from authapp.models import User
from .serializers import AppUsersSerializer


class AppUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AppUsersSerializer
