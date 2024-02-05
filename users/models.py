from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    wallet = models.CharField(max_length=255, unique=True, null=True, blank=True) #WALLET ADDRESS OF THE USER
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    lastMissionDeletionDate = models.DateTimeField(null=True, blank=True, max_length=50)
    # deviceId = models.CharField(max_length=255, null=True, blank=True) #DEVICE ID OF THE USER
    
    REQUIRED_FIELDS = []

    