# Generated by Django 4.0.2 on 2022-02-09 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0006_remove_assignment_assignment_archived_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentassignment',
            name='assignment_prev_status',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
