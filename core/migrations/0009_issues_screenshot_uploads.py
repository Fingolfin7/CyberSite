# Generated by Django 3.2.9 on 2022-06-30 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20220630_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='issues',
            name='screenshot_uploads',
            field=models.ImageField(blank=True, upload_to='Cases/Screenshots'),
        ),
    ]
