from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from wall.models import Writer
from utility.byte2dict import convert


class AccountTests(APITestCase):

    activation_code = ''

    def test_create_account(self):
        """
        Ensure we can create new writer objects.
        """
        url = reverse('writer-registration')
        data = {'name': 'test user1',
                'username': 'testuser1',
                'email': 'test@test.com',
                'phone': '12345',
                'password': 'abcd1234'}
        response = self.client.post(url, data, format='multipart')
        response_data = convert(response.content)
        AccountTests.activation_code = response_data['data']['activation_code']
        self.assertEqual(response_data['status'], 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Writer.objects.count(), 1)
        self.assertEqual(Writer.objects.get(username='testuser1').name, 'test user1')
        data = {'name': 'test user2',
                'username': 'testuser2',
                'email': 'test2@test.com',
                'phone': '567890',
                'password': 'abcd1234'}
        response = self.client.post(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Writer.objects.count(), 2)
        self.assertEqual(Writer.objects.get(username='testuser2').name, 'test user2')
        """
        checking with same username to prevent multiple users with same username or password
        """
        data = {'name': 'test user2',
                'username': 'testuser2',
                'email': 'test2@test.com',
                'phone': '567890',
                'password': 'abcd1234'}
        response = self.client.post(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 400)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Writer.objects.count(), 2)
        self.assertEqual(Writer.objects.get(username='testuser2').name, 'test user2')


class ActivationTests(APITestCase):
    def test_activate_account(self):
        """
        Ensure we can activate new writers objects.
        """
        url = reverse('writer-registration')
        data = {'name': 'test user1',
                'username': 'testuser1',
                'email': 'test@test.com',
                'phone': '12345',
                'password': 'abcd1234'}
        response = self.client.post(url, data, format='multipart')
        response_data = convert(response.content)
        activation_code = response_data['data']['activation_code']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Writer.objects.count(), 1)
        self.assertEqual(Writer.objects.get(username='testuser1').name, 'test user1')
        url = reverse('writer-activation')
        data = {'email': 'test@test.com',
                'auth': '1234'}
        response = self.client.get(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 400)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Writer.objects.count(), 1)
        self.assertEqual(Writer.objects.get(username='testuser1').is_active, False)
        url = reverse('writer-activation')
        data = {'email': 'test@test.com',
                'auth': activation_code}
        response = self.client.get(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Writer.objects.count(), 1)
        self.assertEqual(Writer.objects.get(username='testuser1').is_active, True)