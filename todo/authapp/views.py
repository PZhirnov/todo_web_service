from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from authapp.models import User
from .serializers import AppUsersSerializer
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView, GenericAPIView

# модель User:
# есть возможность просмотра списка
# и каждого пользователя в отдельности, можно вносить изменения, нельзя удалять и создавать;


# class AppUserViewSet(ListAPIView,
#                      RetrieveAPIView,
#                      GenericAPIView):
#     renderer_classes = [JSONRenderer]
#     queryset = User.objects.all()
#     serializer_class = AppUsersSerializer



class AppUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AppUsersSerializer
