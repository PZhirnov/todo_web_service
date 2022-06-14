from django.test import TestCase
import json
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase
from authapp.models import User
from django.contrib.auth import get_user_model
from mainapp.models import Project, UserOnProject, ToDo, Executor
from mainapp.views import ProjectViewSet, UserOnProjectViewSet, ToDoViewSet, ExecutorViewSet
from rest_framework.authtoken.models import Token
from .serializers import ProjectSerializerBase
from mixer.backend.django import mixer
import pdb

# Create your tests here.


class TestProjectViewSet(TestCase):

    def setUp(self):
        self.data = {'name': 'test project2',
                     'description': 'best project',
                     'hrefRepo': 'https://api.nasdaq.com'}

        self.user1 = User.objects.create_superuser(username='Pavel', email='pavel@pavel.ru', password='admin')
        self.user2 = User.objects.create_superuser(username='Elena', email='elena@elena.ru', password='admin')

    def test_get_projects_list(self):
        """
            Используется APIRequestFactory()
        """
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project(self):
        """
            Проверка возможности создания проекта без авторизации
            Используется APIRequestFactory()
        """
        factory = APIRequestFactory()
        request = factory.post(path='/api/projects/', data=self.data, format='json')
        view = ProjectViewSet.as_view({'post': 'create'})
        response = view(request)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_admin(self):
        """
                    Используется APIRequestFactory()
        """
        factory = APIRequestFactory()
        request = factory.post(path='/api/projects/',
                               data=self.data,
                               format='json')
        admin = User.objects.create_superuser(username='admin', email='admin@admin.com',
                                              password='admin111', is_staff=True)
        view = ProjectViewSet.as_view({'post': 'create'})
        token_admin = Token.objects.create(user=admin)
        print(token_admin)
        force_authenticate(request, user=admin, token=f'Token {token_admin}')
        response = view(request)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_put_project_info(self):
        """
            Используется APIClient()
        """
        project = Project.objects.create(name='Test project', description='Test desc')

        project.user_on_project.add(self.user2)
        project.user_on_project.add(self.user1)
        client = APIClient()
        # 1. Проверим доступность информации без авторизации на чтение
        response = client.get(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. проверим наличие пользователей в связанной таблице
        users_on_project = UserOnProject.objects.filter(project=project)
        self.assertTrue(users_on_project.count() > 0)

        # 3. Залогинимся и изменим имя проекта
        client.login(username=self.user1.username, password='admin')
        response_put = client.put(f'/api/projects/{project.id}/',
                                  {'name': 'Update name',
                                   'description': 'new description'})
        self.assertTrue(response_put.status_code, status.HTTP_200_OK)

        # 4. Проверим наличи данные в БД после отправки запроса
        self.assertTrue(Project.objects.get(pk=project.id).name, 'Update name')


# TestCase + API Client  + Mixer
class TestToDoViewSet(TestCase):
    """
        Тут только APIClient()
    """
    def setUp(self):
        self.pwd = 'admin'
        self.admin = User.objects.create_superuser('admin', 'admin@admin.ru', self.pwd)
        self.project = Project.objects.create(name='New Project')
        self.project_id = self.project.id
        # Для тестов от анонимного пользователя
        self.client_anon = APIClient()
        # Для тестов от админа
        self.client = APIClient()

        self.client.login(username=self.admin.username, password=self.pwd)

    def test_get_todo(self):
        # todo = ToDo.objects.create(title='new_todo', project_id=self.project)
        todo = mixer.blend(ToDo, project_id=self.project)
        response = self.client_anon.get(f'/api/todo/{todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Get all Todo
        response = self.client_anon.get(f'/api/todo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_todo_anon(self):
        response = self.client_anon.post(f'/api/todo/', {'title': 'new_todo', 'project_id': self.project_id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_put_todo_admin(self):
        response = self.client.post(f'/api/todo/', {'title': 'new_todo', 'project_id': self.project_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        todo = ToDo.objects.all()[0]
        # pdb.set_trace()
        response = self.client.put(f'/api/todo/{todo.id}/',
                                   {'title': 'update_todo',
                                    'project_id': self.project_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# APITestCase
class TestProjectViewSetAPITest(APITestCase):
    """
       Только APITestCase
    """
    def setUp(self):
        self.admin = User.objects.create_superuser('django', 'django@mail.ru', 'geekbrains')
        self.client.login(username='django', password='geekbrains')
        # self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_admin}')
        self.project = Project.objects.create(name='Проект до редактирования', description='Будет отредактировано')
        self.data = ProjectSerializerBase(self.project).data
        self.data.update({'name': 'test project3', 'description': 'best project',
                          'hrefRepo': 'https://api.nasdaq.com'})

    def test_get_projects(self):
        """
            Проверка возможности получения списка проектов
        """
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_projects(self):
        response = self.client.post('/api/projects/',
                                    {'name': 'New project',
                                     'description': 'Best Project',
                                     'hrefRepo': 'https://api.nasdaq.com'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_delete_project(self):
        """
            Проверка возможности редактирования данных по проекту
        """
        check_val = self.data['name']
        response = self.client.put(f'/api/projects/{self.project.id}/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверим факт изменения данных
        project = Project.objects.get(id=self.project.id)
        self.assertEqual(project.name, check_val)

        # Удалим проект
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


