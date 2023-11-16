from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=255, unique=True) # WALLET PASSWORD
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    lastMissionDeletionDate = models.DateTimeField(null=True, blank=True)
    timeZone = models.CharField(max_length=5)

    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f"{self.username}"