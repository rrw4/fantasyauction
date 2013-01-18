from django.shortcuts import render

from auction.models import Auction
from league.models import League, Roster

def league_home(request, **kwargs):
    league = League.objects.get(id=kwargs.pop('league_id'))
    context = {'league': league}
    return render(request, 'league_home.html', context)

def league_rosters(request, **kwargs):
    league = League.objects.get(id=kwargs.pop('league_id'))
    rosters = Roster.objects.filter(league=league)
    context = {'rosters': rosters}
    return render(request, 'league_rosters.html', context)

def league_auctions(request, **kwargs):
    league = League.objects.get(id=kwargs.pop('league_id'))
    auctions = Auction.objects.filter(league=league)
    context = {'auctions': auctions}
    return render(request, 'league_auctions.html', context)
