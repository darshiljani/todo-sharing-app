from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.db.models import Q

# Create your views here.
class TasksAPI(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, pk=None):
        try:
            if pk is not None:
                task = Tasks.objects.get(id=pk)
                if request.user == task.owner or task.anyone_can_read == True:
                    serializer = TaskSerializer(task, context={"request": request})
                    return Response(data={"status": True, "tasks": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": False, "message": "You do not have the permissions to access the requested task!"}, status=status.HTTP_403_FORBIDDEN)
            else:
                tasks = Tasks.objects.filter(Q(owner=request.user) | Q(anyone_can_read=True)).order_by('id').distinct('id')
                serializer = TaskSerializer(tasks, many=True, context={"request": request})
                return Response(data={"status": True, "tasks": serializer.data}, status=status.HTTP_200_OK)

        except Tasks.DoesNotExist:
            return Response({"status":False, "message": "Task with requested ID does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           print(str(e))
           return Response({"status": False, "message": "There was an error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status": True, "message": "Task added successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
         
    def patch(self, request, pk=None):
        if pk is not None:
            try:
                task = Tasks.objects.get(id=pk)
                if task.owner == request.user:
                    serializer = TaskSerializer(instance=task, data=request.data, context={"request": request}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(data={"status": True, "message": "Task updated successfully!"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(data={"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if task.anyone_can_update:
                        serializer = TaskUpdateApplicationSerializer(data=request.data | {"task": task.id}, context={"request": request})
                        if serializer.is_valid():
                            serializer.save()
                            TaskUpdateLog.objects.create(task=task, message=f"{serializer.validated_data.updated_by.username} has created an update request!")
                            return Response(data={"status": True, "message": "Task update request successful!"}, status=status.HTTP_201_CREATED)
                        else:
                            return Response(data={"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"status": False, "message": "You do not have the permissions to access the requested task!"}, status=status.HTTP_403_FORBIDDEN)
            except Tasks.DoesNotExist:
                return Response(data={"status": False, "message": "Requested task does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"status": False, "message": "There was an error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(data={"status": False, "message": "Task ID not specified!"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
       try:
           task = Tasks.objects.get(pk=pk)
           task.delete()
           return Response({"status": True, "message": "Task deleted successfully!"}, status=status.HTTP_200_OK)
       except Tasks.DoesNotExist:
           return Response({"status": False, "message": "Requested task does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
       except Exception:
           return Response({"status": False, "message": "There was an error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class TaskUpdateApplicationAPI(APIView):
    permission_classes = (IsAuthenticated, )
    
    def patch(self, request, pk=None):
        if pk is not None:
            try:
                task_update_application = TaskUpdateApplications.objects.get(id=pk)
                if task_update_application.task.owner == request.user:
                    serializer = TaskUpdateApplicationEditSerializer(instance=task_update_application, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        if serializer.validated_data.get("is_approved"):
                            task_update_application.task.content = task_update_application.content
                            task_update_application.task.category = task_update_application.category
                            task_update_application.task.due_date = task_update_application.due_date
                            task_update_application.task.save()
                            TaskUpdateLog.objects.create(task=task_update_application.task, message=f"You approved {task_update_application.updated_by.username}'s update request!")
                            return Response(data={"status": True, "message": "Task updated successfully!"}, status=status.HTTP_200_OK)
                        else:
                            return Response(data={"status": True, "message": "Task update rejected!"}, status=status.HTTP_200_OK)
                    else:
                        return Response(data={"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except TaskUpdateApplications.DoesNotExist:
                return Response(data={"status": False, "message": "Requested task update application does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(data={"status": False, "message": "Update application ID not specified!"}, status=status.HTTP_400_BAD_REQUEST)
    
class TaskUpdateLogAPI(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, pk=None):
        if pk is not None:
            logs = TaskUpdateLog.objects.filter(task__id=pk)
            serializer = TaskUpdateLogSerializer(logs, many=True)
            return Response({"status": True, "logs": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": "Please specify task to get logs for!"}, status=status.HTTP_400_BAD_REQUEST)