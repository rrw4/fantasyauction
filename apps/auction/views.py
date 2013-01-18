from django.shortcuts import render

from auction.models import Auction, Bid

def auction_home(request, **kwargs):
    auction = Auction.objects.get(id=kwargs.pop('auction_id'))
    bids = Bid.objects.filter(auction=auction)
    context = {'auction': auction, 'bids': bids}
    return render(request, 'auction_home.html', context)
