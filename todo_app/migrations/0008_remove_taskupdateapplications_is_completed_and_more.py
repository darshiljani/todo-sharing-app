# Generated by Django 4.2.3 on 2023-07-24 19:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0007_taskupdatelog_taskupdateapplications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskupdateapplications',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='taskupdateapplications',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='todo_app.categories'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskupdateapplications',
            name='due_date',
            field=models.DateField(default=datetime.date(2023, 7, 24)),
            preserve_default=False,
        ),
    ]
