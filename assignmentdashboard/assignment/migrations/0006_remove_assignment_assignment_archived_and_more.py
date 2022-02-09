# Generated by Django 4.0.2 on 2022-02-09 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0005_assignment_assignment_course_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='assignment_archived',
        ),
        migrations.AddField(
            model_name='assignment',
            name='students_completed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assignment',
            name='students_in_progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assignment',
            name='students_viewed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='number_of_students',
            field=models.IntegerField(default=0),
        ),
    ]
