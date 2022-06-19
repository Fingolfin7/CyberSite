# Generated by Django 3.2.9 on 2022-04-27 11:15

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('level', models.CharField(choices=[('', 'Level'), ('Intern', 'Intern'), ('Permanent Employee', 'Permanent Employee'), ('Manager', 'Manager')], max_length=100)),
                ('department', models.CharField(choices=[('', 'Department'), ('IT Support', 'IT Support'), ('Digital Forensics', 'Digital Forensics'), ('Cyber Security', 'Cyber Security')], max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
