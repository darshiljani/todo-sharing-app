# Generated by Django 4.2.3 on 2023-07-24 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_alter_tasks_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='todo_app.categories', to_field='name'),
        ),
    ]
