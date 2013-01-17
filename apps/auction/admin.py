from django.contrib import admin

from auction.models import Auction, Bid

admin.site.register(Auction)
admin.site.register(Bid)
