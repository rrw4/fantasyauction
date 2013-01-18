from django.shortcuts import render

from league.models import League

def home(request):
    leagues = League.objects.all()
    context = {'leagues': leagues}
    return render(request, 'home.html', context)
