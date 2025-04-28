# models.py
from django.db import models

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    image_base64 = models.TextField(blank=True, null=True)  # Store the base64 string
    def __str__(self):
        return self.name
