from django.contrib.auth.models import User
from django.db import models

from league.models import League
from player.models import Player

class Auction(models.Model):
    league = models.ForeignKey(League)
    player = models.ForeignKey(Player)
    start_time = models.DateTimeField(blank=True) #server time
    expiration_time = models.DateTimeField(blank=True) #server time
    active = models.BooleanField(default=False) #True when auction is live
    completed = models.BooleanField(default=False) #True when auction has completed

    #denormalized fields
    high_bid_value = models.IntegerField(blank=True)
    high_bidder = models.ForeignKey(User, blank=True)

    def __unicode__(self):
        return self.player.name

class Bid(models.Model):
    auction = models.ForeignKey(Auction)
    bidder = models.ForeignKey(User)
    current_value = models.IntegerField()
    max_value = models.IntegerField()
    current_high_bid = models.BooleanField(default=False) #whether this is current high bid, for an active auction
    winning_bid = models.BooleanField(default=False) #whether this is winning bid for a completed auction

    def __unicode__(self):
        return self.bidder.username + ', ' + self.auction.player.name + ', ' + self.current_value + ', ' + self.max_value
