from django.db import models
from users.models import User

class Mission(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=25, null=True)
    startDate = models.DateTimeField(null=True, max_length=50)
    startTimezone = models.CharField(max_length=50, null=True, blank=True) #'America/Los_Angeles'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    prevDate = models.DateTimeField(blank=True,null=True, max_length=50)
    numberOfDays = models.IntegerField(default=0)
    