from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, unique=True)
    wallet = models.CharField(max_length=255, unique=True) #WALLET ADDRESS OF THE USER
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    lastMissionDeletionDate = models.DateTimeField(null=True, blank=True)
    timeZone = models.CharField(max_length=5)

    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"