from django.urls import path
from task.views import (
    TaskApiView,
    TaskDetailApiView,
)

urlpatterns = [
    path('', TaskApiView.as_view(), name="task_api"),
    path('<int:task_id>', TaskDetailApiView.as_view(), name="task_detail_api"),
]
