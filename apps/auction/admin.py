from django.contrib import admin

from auction.models import Auction, UFAAuction, Bid

admin.site.register(Auction)
admin.site.register(UFAAuction)
admin.site.register(Bid)
