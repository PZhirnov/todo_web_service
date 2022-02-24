from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from authapp.models import ApiUser
from .serializers import AppUsersSerializer


class AppUserViewSet(ModelViewSet):
    queryset = ApiUser.objects.all()
    serializer_class = AppUsersSerializer
