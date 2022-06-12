from task.models import Task
import task.serializers
from rest_framework import status
from utils.utils import BaseAPIView

import logging
logger = logging.getLogger('django')


class TaskApiView(BaseAPIView):
    serializer_class = task.serializers.TaskSerializer

    # 1. List all
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.select_related('user').all()
        task_serializer = self.serializer_class(tasks, many=True)

        logger.info("Tasks retreived successfully")
        return self.success_response(payload=task_serializer.data, description="Tasks retreived successfully")

    # 2. Create
    def post(self, request, *args, **kwargs):
        task_serializer = self.serializer_class(data=request.data)

        if not task_serializer.is_valid():
            logger.error("Unable to add task")
            return self.bad_request_response(error=task_serializer.errors, description="Unable to add task")

        task_serializer.save()
        logger.info("Task added successfully")
        return self.success_response(payload=task_serializer.data, description="Task added successfully")


class TaskDetailApiView(BaseAPIView):
    serializer_class = task.serializers.TaskSerializer

    # 3. Retrieve
    def get(self, request, task_id, *args, **kwargs):
        task_instance = Task.get_object(task_id)

        if not task_instance:
            logger.error("Object with task id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive task")

        task_serializer = self.serializer_class(task_instance)
        logger.info("Task retreived successfully")
        return self.success_response(payload=task_serializer.data, description="Task retrieved successfully")

    # 4. Update
    def put(self, request, task_id, *args, **kwargs):
        task_instance = Task.get_object(task_id)

        if not task_instance:
            logger.error("Object with task id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive task")

        task_serializer = self.serializer_class(
            instance=task_instance, data=request.data, partial=True)

        if not task_serializer.is_valid():
            return self.bad_request_response(error=task_serializer.errors, description="Unable to update task")

        task_serializer.save()
        logger.info("Task updated successfully")
        return self.success_response(payload=task_serializer.data, description="Task updated successfully")


    # 5. Delete
    def delete(self, request, task_id, *args, **kwargs):
        task_instance = Task.get_object(task_id)

        if not task_instance:
            logger.error("Object with task id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive task")

        task_instance.delete()
        logger.info("Task Deleted")
        return self.success_response(payload={}, description="Task deleted successfully")
