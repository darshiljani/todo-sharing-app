from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = Tasks
        fields = "__all__"
        
class TaskUpdateApplicationSerializer(serializers.ModelSerializer):
    updated_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = TaskUpdateApplications
        fields = "__all__"
        
class TaskUpdateApplicationEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUpdateApplications
        fields = ("is_approved", )
        
class TaskUpdateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUpdateLog
        fields = "__all__"