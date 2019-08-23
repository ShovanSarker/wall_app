from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from wall.models import Writer
from wall.models import Post

from utility.byte2dict import convert


class CompleteTests(APITestCase):
    def test_process(self):
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
        print('Registration => Checked')
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
        print('Multiple used with same username prevented => Checked')
        url = reverse('writer-activation')
        data = {'email': 'test@test.com',
                'auth': '1234'}
        response = self.client.get(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 400)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Writer.objects.count(), 2)
        self.assertEqual(Writer.objects.get(username='testuser1').is_active, False)
        print('Activation attempt with wrong code prevented => Checked')
        url = reverse('writer-activation')
        data = {'email': 'test@test.com',
                'auth': activation_code}
        response = self.client.get(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Writer.objects.count(), 2)
        self.assertEqual(Writer.objects.get(username='testuser1').is_active, True)
        print('Activation with code succeeded => Checked')
        url = reverse('writer-login')
        data = {'email': 'test@test.com',
                'password': 'abcd123'}
        response = self.client.post(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 400)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Login with incorrect credentials prevented => Checked')
        url = reverse('writer-login')
        data = {'email': 'test@test.com',
                'password': 'abcd1234'}
        response = self.client.post(url, data, format='multipart')
        response_data = convert(response.content)
        session_id = response_data['data']['sid']
        self.assertEqual(response_data['status'], 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Login with correct credentials succeeded => Checked')
        url = reverse('post-create')
        data = {'sid': '318ec9db-6b6e-46cf-8c60-cae89a7b0ae2',
                'title': 'Test Article',
                'content': 'This is a test article'}
        response = self.client.post(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 400)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 0)
        print('Posting on wall with incorrect session id prevented => Checked')
        url = reverse('post-create')
        data = {'sid': session_id,
                'title': 'Test Article',
                'content': 'This is a test article'}
        response = self.client.post(url, data, format='multipart')
        response_data = convert(response.content)
        self.assertEqual(response_data['status'], 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(title='Test Article').published, True)
        print('Posting on wall with correct session id succeeded => Checked')
