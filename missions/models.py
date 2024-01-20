from django.db import models
from users.models import User

class Mission(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=25, null=True)
    startDate = models.CharField(null=True, max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    isCompleted = models.BooleanField(default=False) #in mission creation we set isCompleted to False
    prevDate = models.CharField(blank=True,null=True, max_length=30)
    numberOfDays = models.IntegerField(default=0)
    