from django.test import TestCase
import json
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase
from django.contrib.auth.models import User
from mainapp.views import ProjectViewSet, UserOnProjectViewSet, ToDoViewSet, ExecutorViewSet

# Create your tests here.


class TestProjectViewSet(TestCase):

    def test_get_projects_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

