from django.test import TestCase
import json
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase
from authapp.models import User
from mainapp.models import Project, UserOnProject, ToDo, Executor
from mainapp.views import ProjectViewSet, UserOnProjectViewSet, ToDoViewSet, ExecutorViewSet
from rest_framework.authtoken.models import Token

# Create your tests here.


class TestProjectViewSet(TestCase):

    # def test_get_projects_list(self):
    #     factory = APIRequestFactory()
    #     request = factory.get('/api/projects/')
    #     view = ProjectViewSet.as_view({'get': 'list'})
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_create_project(self):
    #     '''
    #         Проверка возможности создания проекта без авторизации
    #     '''
    #     factory = APIRequestFactory()
    #     request = factory.post(path='/api/projects/', data=
    #                            {'name': 'test project2', 'description': 'best project',
    #                             'hrefRepo': 'https://api.nasdaq.com'}, format='json')
    #     view = ProjectViewSet.as_view({'post': 'create'})
    #     response = view(request)
    #     print(response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_create_project_admin(self):
    #     factory = APIRequestFactory()
    #     request = factory.post(path='/api/projects/', data={'name': 'test project3', 'description': 'best project',
    #                                                     'hrefRepo': 'https://api.nasdaq.com'}, format='json')
    #     admin = User.objects.create_superuser(username='admin', email='admin@admin.com',
    #                                           password='admin111', is_staff=True)
    #     print(admin.id, admin.is_staff, admin.is_superuser, admin.is_active)
    #     view = ProjectViewSet.as_view({'post': 'create'})
    #     token_admin = Token.objects.create(user=admin)
    #     print(token_admin)
    #     force_authenticate(request, user=admin, token=f'Token {token_admin}')
    #     response = view(request)
    #     print(response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_project_info(self):
        '''
            Используется APIClient()
        '''
        project = Project.objects.create(name='Test project', description='Test desc')
        user1 = User.objects.create_superuser(username='Pavel', email='pavel@pavel.ru', password='1234')
        user2 = User.objects.create_superuser(username='Elena', email='elena@elena.ru', password='5678')
        project.user_on_project.add(user2)
        project.user_on_project.add(user1)
        client = APIClient()
        # 1. Проверим доступность информации без авторизации на чтение
        response = client.get(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. проверим наличие пользователей в связанной таблице
        users_on_project = UserOnProject.objects.filter(project=project)
        self.assertTrue(users_on_project.count() > 0)

        # 3. Залогинимся и изменим имя проекта
        client.login(username='Pavel', password='1234')
        response_put = client.put(f'/api/projects/{project.id}/',
                                  {'name': 'Update name',
                                   'description': 'new description'})
        self.assertTrue(response_put.status_code, status.HTTP_200_OK)

        # 4. Проверим наличи данные в БД после отправки запроса
        self.assertTrue(Project.objects.get(pk=project.id).name, 'Update name')


class TestToDoViewSet(TestCase):

    def test_get_todo_list(self):
        '''
            Проверка получения TODO без авторизации
        '''
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
