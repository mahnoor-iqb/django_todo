from django.urls import path
from task.views import (
    TaskApiView,
    TaskDetailApiView
)

urlpatterns = [
    path('tasks', TaskApiView.as_view()),
    path('tasks/<int:task_id>', TaskDetailApiView.as_view()),
]
