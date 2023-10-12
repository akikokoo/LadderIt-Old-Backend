from django.db import models


class User(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    password = models.CharField()
    