from django.contrib.auth.models import User
from django.db import models

class League(models.Model):
    name = models.CharField(max_length=100, blank=True)
    users = models.ManyToManyField(User, blank=True)
    size = models.IntegerField(default=0)

class Roster(models.Model):
    league = models.ForeignKey(League)
    user = models.ForeignKey(User)
