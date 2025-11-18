from django.db import models
from django.contrib.auth.models import User
from home_setup.models import Department

# Create your models here.

class Profile(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type} - {self.department}"