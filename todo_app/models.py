from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=20, unique=True)
        
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self) -> str:
        return self.name
    
class Tasks(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    category = models.ForeignKey(to=Categories, to_field='name', on_delete=models.DO_NOTHING)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    anyone_can_read = models.BooleanField(default=False)
    anyone_can_update = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.content
    
    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
        ordering = ['-due_date']
        
class TaskUpdateApplications(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    due_date = models.DateField()
    is_approved = models.BooleanField(null=True)
    

class TaskUpdateLog(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    