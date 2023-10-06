
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_instructor = models.BooleanField(default=False)  # A flag to differentiate roles

class Course(models.Model):
    name = models.CharField(max_length=255)
    age_range = models.CharField(max_length=50)
    course_id = models.CharField(max_length=20, unique=True)
    # Add other course-specific fields like description, start date, etc.
