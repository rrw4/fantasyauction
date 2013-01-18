from django.contrib.auth.models import User
from django.db import models

from league.models import League
from player.models import Player

class Auction(models.Model):
    league = models.ForeignKey(League)
    player = models.ForeignKey(Player)
    start_time = models.DateTimeField(blank=True) #server time
    expiration_time = models.DateTimeField(blank=True) #server time

    def __unicode__(self):
        return self.player.name

class Bid(models.Model):
    auction = models.ForeignKey(Auction)
    bidder = models.ForeignKey(User)
    current_value = models.FloatField()
    max_value = models.FloatField()
    winning_bid = models.BooleanField(default=False)

    def __unicode__(self):
        return self.bidder.username + ', ' + self.auction.player.name + ', ' + self.current_value + ', ' + self.max_value
