"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authapp.views import AppUserViewSet
from mainapp.views import ProjectViewSet, ToDoViewSet, UserOnProjectViewSet, ExecutorViewSet
from authapp.views import AppUserViewSet

router = DefaultRouter()
# router.register('users', AppUserViewSet, basename='users')
router.register('projects', ProjectViewSet)
router.register('todo', ToDoViewSet, basename='todo')
router.register('users_on_project', UserOnProjectViewSet)
router.register('executors', ExecutorViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('users/', AppUserViewSet.as_view()),
    # path('api/todo/<int:pk>', ToDoViewSet.as_view({'get': 'list'})),
    # path('api/todo/', ToDoViewSet.as_view({'get': 'list'})),
]
