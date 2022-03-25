from django.shortcuts import render
from django.db.models import Count
from . models import League

# Create your views here.
def main(request):
    leagues = League.objects.annotate(games_played=Count('match'))

    return render(request, 'main.html', {'leagues':leagues})

def contact(request):
    return render(request, 'contact.html')

def dashboard(request,slug):
    
    return render(request, 'dashboard.html')