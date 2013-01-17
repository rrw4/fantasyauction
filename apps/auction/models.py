from django.contrib.auth.models import User
from django.db import models

from league.models import League

class Auction(models.Model):
    league = models.ForeignKey(League)
    start_time = models.DateTimeField(blank=True) #server time
    expiration_time = models.DateTimeField(blank=True) #server time

class Bid(models.Model):
    auction = models.ForeignKey(Auction)
    bidder = models.ForeignKey(User)
    current_value = models.FloatField()
    max_value = models.FloatField()
    winning_bid = models.BooleanField(default=False)
