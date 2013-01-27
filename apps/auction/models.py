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
            Four main cases:
            1. No bids yet
               -Sets the made bid as high bidder, and current bid to MIN_BID_VALUE
            1. Existing bids, same bidder as high bidder, and made bid is higher than proxy (max value) of high bid
               -Same high bidder, and proxy (max value) increases, while current bid remains the same
            3. Existing bids, bidder is different than the high bidder, and the made bid is higher than proxy (max value) of highest bid
               -Sets the made bid as high bidder, and current bid to max value of highest bid + MIN_BID_INCREMENT
            4. Existing bids, bidder is different than the high bidder, and the made bid is higher than current bid value but less than 
               proxy (max value) of highest bid
               -Sets the current bid to max value of made bid
        """
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
                #this bid has same bidder as high bidder - high bidder is raising his proxy bid
                if bid.bidder == self.high_bidder:
                    if bid.max_value > high_bid.max_value:
                        #TODO: do something with bid time - this bid is shown in bid history, which clues in other bidders than proxy was raised
                        #remove current_high_bid, but don't change current_value
                        high_bid.remove_current_high_bid()
                        #update the made bid to be current high bid, but current value is same as previous high bid's current value
                        bid.set_current_high_bid()
                        bid.set_current_value(current_value=high_bid.current_value)
                        #don't need to update auction, since high bid value and high bidder remain the same
                    else:
                        #this case should not be hit - would mean bid form allowed invalid bid (same bidder as high bid, and bid
                        #   is less than or equal to max value of high bid)
                        bid.set_current_value(bid.max_value)
                #different bidder than high bidder
                else:
                    #high bid is outbid - new high bid
                    if bid.max_value > high_bid.max_value:
                        #update current high bid
                        high_bid.set_current_value(current_value=high_bid.max_value)
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

    def save(self, *args, **kwargs):
        new_bid = True if self.id is None else False
        super(Bid, self).save(*args, **kwargs)
        #if this is a new bid, make the bid on the auction
        if new_bid:
            auction = self.auction
            auction.make_bid(self)

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
