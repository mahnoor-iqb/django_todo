from task.models import Task
from task.serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

import logging
logger = logging.getLogger('django')

class TaskApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        task_serializer = TaskSerializer(tasks, many=True)
        logger.info("Tasks retreived successfully")
        return Response(task_serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        logger.debug(data)
        task_serializer = TaskSerializer(data=data)
        if task_serializer.is_valid():
            task_serializer.save()
            logger.info("Task added successfully")
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Unable to add task")
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailApiView(APIView):

    # Helper method
    def get_object(self, task_id):
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id)
        if not task_instance:
            logger.error("Object with task id does not exist")
            return Response(
                {"message": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskSerializer(task_instance)

        logger.info("Task retreived successfully")
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id)
        if not task_instance:
            logger.error("Object with task id does not exist")
            return Response(
                {"message": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = JSONParser().parse(request)
        serializer = TaskSerializer(
            instance=task_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Task updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id)
        if not task_instance:
            logger.error("Object with task id does not exist")
            return Response(
                {"message": "Object with task id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task_instance.delete()
        logger.info("Task Deleted")
        return Response(
            {"message": "Object deleted!"},
            status=status.HTTP_200_OK
        )
