# Generated by Django 3.2.9 on 2022-06-30 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_issues_screenshot_uploads'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issues',
            name='screenshot_uploads',
        ),
    ]
