from django.db import models
from users.models import User

class Mission(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    isCompleted = models.BooleanField(default=False) #in mission creation we set isCompleted to False
    prevDate = models.DateTimeField(blank=True,null=True)
    numberOfDays = models.IntegerField(default=0)
    