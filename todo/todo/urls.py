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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from authapp.views import AppUserViewSet
from mainapp.views import ProjectViewSet, ToDoViewSet,  UserOnProjectViewSet, ExecutorViewSet
from authapp.views import AppUserViewSet
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


router = DefaultRouter()
router.register('users', AppUserViewSet, basename='users')
router.register('projects', ProjectViewSet, basename='projects')
router.register('todo', ToDoViewSet)
router.register('users_on_project', UserOnProjectViewSet)
router.register('executors', ExecutorViewSet)

schema_view = get_schema_view(
    openapi.Info(title='ToDo',
                 default_version='2.0',
                 description='Documentation to out project',
                 contact=openapi.Contact(email="admin@admin.local"),
                 license=openapi.License(name="MIT License"),
                 ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

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
    # path('schema/', schema_view),
    # 1 - URLPathVersioning
    # При отправе запроса http://127.0.0.1:8000/api/2.0/users/ будет использовать другой сериализатор
    # re_path(r'^api/(?P<version>\d\.\d)/users/$', AppUserViewSet.as_view({'get': 'list'})),

    # 2 - NamespaceVersioning
    # path('api/users/2.0/', include('authapp.urls', namespace='2.0')),
    # path('api/users/1.0/', include('authapp.urls', namespace='1.0')),

    # Add drf-yasg
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# https://www.django-rest-framework.org/coreapi/schemas/
