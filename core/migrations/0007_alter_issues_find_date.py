# Generated by Django 4.0.5 on 2022-06-24 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_issues_screenshots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='find_date',
            field=models.DateField(),
        ),
    ]
