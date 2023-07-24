from django.urls import path
from .views import *

urlpatterns = [
    path('', TasksAPI.as_view(), name='tasks'),
    path('<int:pk>/', TasksAPI.as_view(), name='task'),
    path('edit-update-application/<int:pk>/', TaskUpdateApplicationAPI.as_view(), name='task-update-application-edit'),
    path('<int:pk>/update-logs/', TaskUpdateLogAPI.as_view(), name='update-logs')
]