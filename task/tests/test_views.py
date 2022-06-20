
from http.client import responses
from typing import OrderedDict
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from task.models import Task
from user.models import User
from datetime import datetime
import pytz
from collections import OrderedDict


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.task_api_url = reverse('task_api')
        self.task_detail_api_url = reverse('task_detail_api', args=[5])

        # Add test user
        self.user = User(email='testuser@gmail.com',
                         password=make_password('testpass'))
        self.user.save()

        # Log in test user
        self.client.post(self.login_url,  {
            'email': 'testuser@gmail.com',
            'password': 'testpass'
        })

        # Add test task
        self.task = Task(id=5, title='Test task',
                         description='Test description',
                         due_date=datetime(2017, 11, 28, 23,
                                           55, 59, 342380, tzinfo=pytz.UTC),
                         user=self.user)
        self.task.save()

    def test_task_api_GET(self):
        response = self.client.get(self.task_api_url)
        error = response.data['error']
        success = response.data['success']

        self.assertEquals(error, {})
        self.assertEquals(success, True)
        self.assertEquals(response.status_code, 200)

    def test_task_detail_api_GET(self):
        response = self.client.get(self.task_detail_api_url)
        error = response.data['error']
        success = response.data['success']

        self.assertEquals(error, {})
        self.assertEquals(success, True)
        self.assertEquals(response.status_code, 200)

    def test_task_detail_api_PUT(self):
        response = self.client.put(self.task_detail_api_url, {
            'title': 'Updated task'
        }, content_type='application/json')

        error = response.data['error']
        success = response.data['success']

        self.assertEquals(error, {})
        self.assertEquals(success, True)
        self.assertEquals(response.status_code, 200)

    def test_task_detail_api_DELETE(self):
        response = self.client.delete(self.task_detail_api_url)
        error = response.data['error']
        success = response.data['success']

        self.assertEquals(error, {})
        self.assertEquals(success, True)
        self.assertEquals(response.status_code, 200)

    def test_task_api_POST(self):
        response = self.client.post(self.task_api_url, {
            'title': 'Create an app',
            'description': 'Create an app using flask',
            'creation_date': "2022-06-01 00:00:00",
            'due_date': "2022-08-01 00:00:00"})
        error = response.data['error']
        success = response.data['success']

        self.assertEquals(error, {})
        self.assertEquals(success, True)
        self.assertEquals(response.status_code, 201)

    def test_task_api_POST_missing_title(self):
        response = self.client.post(self.task_api_url, {
            'description': 'Test Task description',
            'creation_date': "2022-06-01 00:00:00",
            'due_date': "2022-08-01 00:00:00"})
  
        success = response.data['success']
        
        self.assertEquals(success, False)
        self.assertEquals(response.status_code, 400)