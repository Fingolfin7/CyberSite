# Generated by Django 3.2.9 on 2022-06-30 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_issues_screenshot_uploads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='screenshot_uploads',
            field=models.FileField(blank=True, upload_to='Cases/Screenshots'),
        ),
    ]