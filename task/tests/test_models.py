from django.test import TestCase
from task.models import Task
from user.models import User
from datetime import datetime, date
from django.contrib.auth.hashers import make_password

import pytz

class TestModels(TestCase):

    def setUp(self):
        # Add test user
        self.user = User(email='testuser@gmail.com',
                         password=make_password('testpass'))
        self.user.save()

        # Add test task
        self.task = Task(title='Test task',
                          description='Test description',
                         creation_date=datetime(2022, 6, 20, 0, 0, 0, tzinfo=pytz.UTC),
                          due_date=datetime(2022, 7, 12, 0, 0, 0, tzinfo=pytz.UTC),
                          completion_date=None,
                          completion_status = False,
                          file_attachment = 'file.txt',
                          user=self.user)
        self.task.save()

    def test_new_task(self):
        self.assertEquals(self.task.title, "Test task")
        self.assertEquals(self.task.description, "Test description")
        self.assertEquals(self.task.creation_date.date(), date(2022, 6, 20))
        self.assertEquals(self.task.due_date.date(), date(2022, 7, 12))
        self.assertEquals(self.task.completion_date, None)
        self.assertEquals(self.task.completion_status, False)
        self.assertEquals(self.task.file_attachment, "file.txt")
        self.assertEquals(self.task.user, self.user)

