from django.contrib.auth.models import User
from django.db import models

from auction.constants import MIN_BID_VALUE, MIN_BID_INCREMENT
from league.models import League, Roster
from player.models import Player

class Auction(models.Model):
    league = models.ForeignKey(League)
    player = models.ForeignKey(Player)
    start_time = models.DateTimeField(blank=True) #server time
    expiration_time = models.DateTimeField(blank=True) #server time
    active = models.BooleanField(default=False) #True when auction is live
    completed = models.BooleanField(default=False) #True when auction has completed

    #denormalized fields
    high_bid_value = models.IntegerField(blank=True, null=True)
    high_bidder = models.ForeignKey(User, blank=True, null=True)

    def make_bid(self, bid):
        """ Makes a bid on this auction, if it is active
            Will set the bid's current_value
            Three main cases:
            1. No bids yet
               -Sets the made bid as high bidder, and current bid to MIN_BID_VALUE
            2. Existing bids, and the made bid is higher than proxy (max value) of highest bid
               -Sets the made bid as high bidder, and current bid to max value of highest bid + MIN_BID_INCREMENT
            3. Existing bids, and the made bid is higher than current bid value but less than proxy (max value) of highest bid
               -Sets the current bid to max value of made bid
        """
        #TODO: allow increasing of high bidder's proxy bid
        if self.active and bid != None and bid.auction == self:
            #first bid
            if self.high_bidder == None and bid.max_value >= MIN_BID_VALUE:
                bid.set_current_high_bid()
                bid.set_current_value(current_value=MIN_BID_VALUE)
                self.high_bid_value = MIN_BID_VALUE
                self.high_bidder = bid.bidder
            #previous bids have been made
            else:
                high_bid = self.get_high_bid()
                #high bid is outbid - new high bid
                if bid.max_value > high_bid.max_value:
                    #update current high bid
                    high_bid.set_current_value(high_bid.max_value)
                    high_bid.remove_current_high_bid()
                    #update the made bid to be current high bid
                    bid.set_current_high_bid()
                    bid.set_current_value(current_value=high_bid.max_value+MIN_BID_INCREMENT)
                    #update auction to have correct denormalized fields
                    self.high_bid_value = bid.current_value
                    self.high_bidder = bid.bidder
                #high bid is not outbid - increase current value if needed
                else:
                    if bid.max_value > high_bid.current_value:
                        high_bid.set_current_value(bid.max_value)
                        bid.set_current_value(bid.max_value)
                        self.high_bid_value = bid.max_value
                    else:
                        #this case should not be hit - would mean bid form allowed invalid bid (less than or equal to current high bid)
                        bid.set_current_value(bid.max_value)
            self.save()

    def complete(self):
        """ Completes the auction if it is not already completed:
            -Set completed to True
            -If there is a high bidder, adds the player to the high bidder's roster
            -Sets Bid with current_high_bid = True to winning_bid = True
        """
        if not self.completed:
            self.completed = True
            self.active = False
            if self.high_bidder != None:
                roster = Roster.objects.get(user=self.high_bidder)
                roster.add_player(player=self.player, salary=self.high_bid_value)
                high_bid = self.get_high_bid()
                high_bid.set_winning_bid()
            self.save()

    def get_high_bid(self):
        """ Returns Bid object of high bid """
        try:
            high_bid = Bid.objects.get(auction=self, current_high_bid=True)
        except Bid.DoesNotExist:
            return None
        return high_bid

    def __unicode__(self):
        return self.player.name

class Bid(models.Model):
    auction = models.ForeignKey(Auction)
    bidder = models.ForeignKey(User)
    time = models.DateTimeField(blank=True) #server time
    current_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField()
    current_high_bid = models.BooleanField(default=False) #whether this is current high bid, for an active auction
    winning_bid = models.BooleanField(default=False) #whether this is winning bid for a completed auction

    def set_current_value(self, current_value):
        if self.current_value != current_value:
            self.current_value = current_value
            self.save()

    def set_current_high_bid(self):
        if self.current_high_bid != True:
            self.current_high_bid = True
            self.save()

    def set_winning_bid(self):
        if self.winning_bid != True:
            self.winning_bid = True
            self.save()

    def remove_current_high_bid(self):
        if self.current_high_bid != False:
            self.current_high_bid = False
            self.save()

    def __unicode__(self):
        return self.bidder.username + ', ' + self.auction.player.name + ', ' + str(self.time)

#TODO: post_save signal when bid is created to call auction.make_bid()
