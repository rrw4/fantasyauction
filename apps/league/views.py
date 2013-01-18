from django.shortcuts import render

from league.models import League

def league_home(request, **kwargs):
    league = League.objects.get(id=kwargs.pop('league_id'))
    context = {'league': league}
    return render(request, 'league_home.html', context)

def league_rosters(request, **kwargs):
    return render(request, 'league_rosters.html')

def league_auctions(request, **kwargs):
    return render(request, 'league_auctions.html')
