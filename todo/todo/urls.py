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
from mainapp.views import ProjectViewSet, ToDoViewSet,  UserOnProjectViewSet, ExecutorViewSet
from authapp.views import AppUserViewSet
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.schemas import get_schema_view


router = DefaultRouter()
router.register('users', AppUserViewSet, basename='users')
router.register('projects', ProjectViewSet, basename='projects')
router.register('todo', ToDoViewSet)
router.register('users_on_project', UserOnProjectViewSet)
router.register('executors', ExecutorViewSet)

schema_view = get_schema_view(title="Example API")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/users/', AppUserViewSet.as_view()),
    # path('api/todo/<int:pk>', ToDoViewSet.as_view({'get': 'list'})),
    # path('api/todo/', ToDoViewSet.as_view({'get': 'list'})),
    path('schema/', schema_view),
]

# https://www.django-rest-framework.org/coreapi/schemas/
