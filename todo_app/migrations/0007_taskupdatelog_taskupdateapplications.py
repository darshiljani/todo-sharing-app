# Generated by Django 4.2.3 on 2023-07-24 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo_app', '0006_tasks_anyone_can_read_tasks_anyone_can_update_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskUpdateLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo_app.tasks')),
            ],
        ),
        migrations.CreateModel(
            name='TaskUpdateApplications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo_app.tasks')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]