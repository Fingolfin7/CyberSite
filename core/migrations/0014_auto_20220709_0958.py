# Generated by Django 3.2.9 on 2022-07-09 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_issues_severity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issues',
            old_name='summary',
            new_name='impact',
        ),
        migrations.AddField(
            model_name='issues',
            name='affected_hosts',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='issues',
            name='solution',
            field=models.TextField(blank=True),
        ),
    ]
