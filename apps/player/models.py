from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100, blank=True)
    team = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
