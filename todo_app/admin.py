from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name", )
    
@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('owner', 'content', 'category', 'due_date', 'is_completed', 'anyone_can_read', 'anyone_can_update')

@admin.register(TaskUpdateApplications)
class TaskUpdateApplicationsAdmin(admin.ModelAdmin):
    list_display = ("task", "updated_by", "content", "category", "due_date", "is_approved")
