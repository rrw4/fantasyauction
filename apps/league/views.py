from django.shortcuts import render

def league_home(request, **kwargs):
    return render(request, 'league_home.html')

def league_rosters(request, **kwargs):
    return render(request, 'league_rosters.html')

def league_auctions(request, **kwargs):
    return render(request, 'league_auctions.html')
