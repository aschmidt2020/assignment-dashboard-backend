# Generated by Django 4.0.2 on 2022-02-17 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0014_alter_assignment_assignment_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assignment_desc',
            field=models.TextField(default=None),
        ),
    ]