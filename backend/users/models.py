from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None  # Disable the username field

    email = models.EmailField(unique=True)  # Ensure email is unique
    usn = models.CharField(max_length=15, unique=True)

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('HOD', 'HOD'),
        ('PRINCIPAL', 'Principal'),
        ('STUDENT', 'Student'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    usn = models.CharField(max_length=12, blank=True, null=True)  # Only for Students
    branch = models.CharField(max_length=100, blank=True, null=True)  # Only for HOD/Admin

    EMAIL_FIELD = 'email'  # Use email as the unique identifier
    USERNAME_FIELD = 'email'  # Set the username field to email
    REQUIRED_FIELDS = ['role']  # Specify required fields

    def __str__(self):
        return self.email
