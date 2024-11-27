from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    TYPE_CHOICES = [("S", "Student"), ("E", "Employee")]
    user_type = models.CharField(
        max_length=1, choices=TYPE_CHOICES
    )  # to store user_type if user is student or Employee
