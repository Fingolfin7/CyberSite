# Generated by Django 3.2.9 on 2022-10-14 23:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20220820_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='logo',
            field=models.ImageField(max_length=500, upload_to='Cases/Logos'),
        ),
        migrations.AlterField(
            model_name='poc',
            name='image',
            field=models.ImageField(blank=True, max_length=500, upload_to='Cases/Screenshots', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jfif', 'exif', 'gif', 'tiff', 'bmp'])]),
        ),
    ]
