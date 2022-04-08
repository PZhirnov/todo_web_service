from django.shortcuts import render
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from authapp.models import User
from .serializers import AppUsersSerializer, AppUsersExtendedSerializer
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
#     permission_classes = [permissions.IsAuthenticated]


class AppUserViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = User.objects.all()
    serializer_class = AppUsersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.version == '2.0.1':
            return AppUsersExtendedSerializer
        AppUsersSerializer
