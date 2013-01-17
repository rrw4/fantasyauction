from django.shortcuts import render

def auction_home(request, **kwargs):
    return render(request, 'auction_home.html')
