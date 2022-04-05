from django.test import TestCase
from requests import request, post, get
# Create your tests here.
from rest_framework.test import CoreAPIClient


class TestToken(TestCase):
    '''
        Проверка создания и получения токенов на работающем сервере
    '''

    def setUp(self):
        self.data = {'username': 'django', 'password': 'geekbrains'}
        self.password = 'geekbrains'
        self.url_token = 'http://127.0.0.1:8000/api-token-auth/'
        self.url_token_jwt = 'http://127.0.0.1:8000/api/token/'
        self.url_test = 'http://127.0.0.1:8000/api/projects/'

    def test_response_no_token(self):
        # Запрос без токена
        response = post(self.url_test)
        self.assertEqual(response.status_code, 401)

    def test_token(self):
        # Авторизация по токену
        response = post(self.url_token, data=self.data)
        self.assertEqual(response.status_code, 200)
        token = response.json().get('token')
        response_test = get(self.url_test, headers={'Authorization': f'Token {token}'})
        self.assertEqual(response_test.status_code, 200)

    def test_token_jwt(self):
        # Авторизация по JWT токену
        response = post(self.url_token_jwt, data=self.data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        token_access = response_json.get('access')
        token_refresh = response_json.get('refresh')
        # Проверка access токена
        response_test = get(self.url_test, headers={'Authorization': f'Bearer {token_access}'})
        self.assertEqual(response_test.status_code, 200)
        # Проверка refresh токена и сравнение со старым - не должны быть одинаковыми
        response_refresh = post(self.url_token_jwt, data={'refresh': token_refresh})
        token_access_refresh = response_refresh.json().get('access')
        self.assertNotEqual(token_access, token_access_refresh)

# import coreapi

from coreapi import Client


class LiveTest(TestCase):

    def setUp(self):
        self.data = {'name': 'test project2',
                     'description': 'best project',
                     'hrefRepo': 'https://api.nasdaq.com'}

    def test_first(self):
        # Fetch the API schema
        client = Client()
        document = client.get('http://127.0.0.1:8000/schema/')
        print(type(document))
        # client.action(document, ['projects', 'create'], params=self.data)
        #print(data)



        # # Создадим новый проект
        # params = self.data
        # client.action(schema, ['projects', 'create'], params)
        #
        # # Ensure that the organisation exists in the listing
        # data = client.action(schema, ['projects', 'list'])
        # assert (len(data) == 1)
        # # assert (data == [{'name': 'MegaCorp', 'status': 'active'}])

