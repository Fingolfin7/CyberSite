from django.db import models
from django.contrib.auth.models import User
from PIL import Image

levelChoices = [
        ("", "Level"),
        ("Intern", "Intern"),
        ("Permanent Employee", "Permanent Employee"),
        ("Manager", "Manager"),
    ]


departmentChoices = [
        ("", "Department"),
        ("IT Support", "IT Support"),
        ("Digital Forensics", "Digital Forensics"),
        ("Cyber Security", "Cyber Security"),
    ]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    level = models.CharField(max_length=100, choices=levelChoices)
    department = models.CharField(max_length=100, choices=departmentChoices)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
