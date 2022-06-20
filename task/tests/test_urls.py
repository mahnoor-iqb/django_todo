from django.test import SimpleTestCase
from django.urls import reverse, resolve
from task.views import TaskApiView, TaskDetailApiView

class TestUrls(SimpleTestCase):
    
    def test_task_api_resolves(self):
        url = reverse('task-v1:task_api')
        self.assertEquals(resolve(url).func.view_class, TaskApiView)

    def test_task_detail_api_resolves(self):
        url = reverse('task-v1:task_detail_api', args=[1])
        self.assertEquals(resolve(url).func.view_class, TaskDetailApiView)