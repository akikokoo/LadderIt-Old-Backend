from django.db import models
from users.models import User

class Mission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="missions")
    title = models.CharField(max_length=255)
    isCompleted = models.BooleanField(default=False) #in mission creation we set isCompleted to False
    prevDate = models.DateTimeField()
    numberOfDays = models.IntegerField(default=0)
    timeZone = models.CharField(max_length=5)