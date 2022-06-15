# Generated by Django 4.0.5 on 2022-06-14 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(null=True)),
                ('completion_date', models.DateTimeField(null=True)),
                ('completion_status', models.BooleanField(default=False)),
                ('file_attachment', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tasks',
            },
        ),
    ]
