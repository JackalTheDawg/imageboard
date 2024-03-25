from core.views import CreateUser, ApplicationInterface
from core.models import *
from rest_framework.test import APITestCase
from rest_framework import status


class RequestTests(APITestCase):

    default_address = 'http://127.0.0.1/'

    data = {
        'email': 'test@mail.com',
        'password': 'verysecretpass',
        'name': 'John',
        'surname': 'Bonjorno',
        'gender': 'dolphin',
        'birthday': '1909-09-09'
    }


    def test_create_account(self):
        """Testing creation account without setup"""
        url = self.default_address + 'registration'

        regestration_request_data = {
            'email': 'anothertest@mail.com',
            'password': 'superverysecretpass',
            'name': 'Elton',
            'surname': 'John',
            'gender': 'unicorn',
            'birthday': '2009-09-29'
        }

        response = self.client.post(url, regestration_request_data, format='json')
        user = CustomUser.objects.get(email=regestration_request_data['email'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, regestration_request_data['email'])
        self.assertEqual(user.profile.name, regestration_request_data['name'])


    def setUp(self):
        """Creation user for testing requests and JWT tokens"""
        user = CustomUser.objects.create_user(
            email=self.data['email'],
            password=self.data['password'],
            is_active=True
        )

        Profile.objects.create(
            user=user,
            name=self.data['name'],
            surname=self.data['surname'],
            birthday=self.data['birthday'],
            gender=self.data['gender']
        )

        Community.objects.create(
            name='SomeMemes',
        )



    def test_case_one(self):
        """request without token"""
        response_without_token = self.client.get(self.default_address + 'api/v1/profiles', self.data)
        self.assertEqual(response_without_token.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_case_two(self):
        """get requests with token"""

        token = self.client.post(self.default_address + 'auth/jwt/create', data={
            'email': self.data['email'],
            'password': self.data['password']
        }, format='json')

        user = CustomUser.objects.get(email=self.data['email'])
        community = Community.objects.get(name='SomeMemes')

        urls = [
            'api/v1/profiles',
            'api/v1/communities',
            f'api/v1/profile={user.id}',
            f'api/v1/community={community.id}',
            'api/v1/favorites',
            'api/v1/uncorrect_address',
        ]

        for url in urls:
            response = self.client.get(self.default_address + url, headers={
                'Authorization': 'JWT ' + token.data['access']
            })


            if url != 'api/v1/uncorrect_address':
                self.assertEqual(response.status_code, status.HTTP_200_OK)
            else:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_case_three(self):
        token = self.client.post(self.default_address + 'auth/jwt/create', data={
            'email': self.data['email'],
            'password': self.data['password']
        }, format='json')

        response = self.client.get(self.default_address + '/api/v1/', headers={
            'Authorization': 'JWT ' + token.data['access']
        })

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_case_four(self):
        token = self.client.post(self.default_address + 'auth/jwt/create', data={
            'email': self.data['email'],
            'password': self.data['password']
        }, format='json')



        data = {
            'text': 'lorem ipsum',
            'location': CustomUser.objects.get(email=self.data['email']).id,
        }

        create_post = self.client.post(self.default_address + 'api/v1/', data, format='json', headers={
            'Authorization': 'JWT ' + token.data['access'],
            'Type': 'send-post'
        })

        self.assertEqual(create_post.status_code, status.HTTP_200_OK)
