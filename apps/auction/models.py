from django.contrib.auth.models import User
from django.db import models

from auction.constants import MIN_BID_VALUE, MIN_BID_INCREMENT, NONE, UPCOMING, LIVE, PENDING, COMPLETED
from league.models import League, Season, Roster
from player.models import Player

class Auction(models.Model):
    """ Represents an auction for a player
        Fields:
            league - the league the auction is in
            season - the season the auction is in
            player - the player the auction is for
            start_time - when the auction starts (when it is active and bids can be made)
            expiration_time - when the auction ends (when it is no longer active and bids cannot be made)
            state - state of the auction (NONE, UPCOMING, LIVE, PENDING, or COMPLETED)
            high_bid_value - the currently winning bid.  minimum bid is this value + MIN_BID_INCREMENT (usually 1)
            high_bidder - user that has the currently winning bid
    """
    league = models.ForeignKey(League)
    season = models.ForeignKey(Season)
    player = models.ForeignKey(Player)
    start_time = models.DateTimeField(blank=True) #server time
    expiration_time = models.DateTimeField(blank=True) #server time

    STATE_CHOICES = (
        (NONE, 'None'),
        (UPCOMING, 'Upcoming'),
        (LIVE, 'Live'),
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    )
    state = models.IntegerField(choices=STATE_CHOICES, default=NONE)

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
        if self.is_live() and bid != None and bid.auction == self:
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
            -Change state to COMPLETED
            -If there is a high bidder, adds the player to the high bidder's roster
            -Sets Bid with current_high_bid = True to winning_bid = True
        """
        if not self.is_completed():
            self.set_completed()
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

    def is_live(self):
        return True if self.state == LIVE else False

    def is_completed(self):
        return True if self.state == COMPLETED else False

    def set_upcoming(self):
        if self.state != UPCOMING:
            self.state = UPCOMING
            self.save()

    def set_live(self):
        if self.state != LIVE:
            self.state = LIVE
            self.save()

    def set_pending(self):
        if self.state != PENDING:
            self.state = PENDING
            self.save()

    def set_completed(self):
        if self.state != COMPLETED:
            self.state = COMPLETED
            self.save()

    def __unicode__(self):
        return self.player.name

class Bid(models.Model):
    """ Represents a bid on an auction
        Fields:
            auction - auction this bid is for
            bidder - user that made the bid
            time - time the bid was made
            current_value - the bid's current value in the auction.  if it is the high bid, then this is the previous max +
                MIN_BID_INCREMENT.  if it is not the high bid, this isn't really relevant, but we will still update it (if
                the bid was outbid, current_value = max_value.  this is not set when user enters the bid via the bid form,
                it is only set when the bid is made on the auction via make_bid().
            max_value - the "proxy value" of the bid, e.g. the max the bidder is willing to bid
            current_high_bid - True if this bid is the currently winning bid.  for the bids in an auction, only one bid should
                have this be True
            winning_bid - True if this bid won the auction, e.g. was high bid when auction completed
    """
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
