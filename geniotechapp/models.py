
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_instructor = models.BooleanField(default=False)  # A flag to differentiate roles
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # Set the USERNAME_FIELD to 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add any additional required fields for user creation

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price_individual = models.DecimalField(max_digits=10, decimal_places=2)
    price_group = models.DecimalField(max_digits=10, decimal_places=2)
    from_age = models.PositiveIntegerField()
    to_age = models.PositiveIntegerField()
    enrolled_students = models.JSONField(default=dict)

    def __str__(self):
        return self.title

from django.db import models


class Instructor(CustomUser):
    course_taught = models.CharField(max_length=255, null=True, blank=True)
    students_taught = models.JSONField(default=dict)
    availability = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"


class TimeSlot(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} {self.start_time} - {self.end_time}"
    
class TimeSlotAssignment(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    zoom_link = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self):
        return f" By {self.instructor.full_name} - On Time: {self.timeslot}"

