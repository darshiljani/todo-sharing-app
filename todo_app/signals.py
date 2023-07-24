from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskUpdateApplications, Tasks, TaskUpdateLog

@receiver(post_save, sender=TaskUpdateApplications)
def update_task(sender, **kwargs):
    



