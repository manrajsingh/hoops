import math
from django.forms import IntegerField
from django.shortcuts import render, HttpResponse
from django.db.models import Count, Avg, DateField, Window, F, Q, FloatField, Max, Subquery, OuterRef
from django.db.models.functions import RowNumber, Cast
from . models import League, Match, Player, PlayerStats

# Create your views here.
def main(request):
    leagues = League.objects.annotate(games_played=Count('match'))

    return render(request, 'main.html', {'leagues':leagues})

def contact(request):
    return render(request, 'contact.html')

def dashboard(request,slug):
    context = {
        'slug': slug,
    }
    return render(request, 'dashboard.html', context)

def games_played(request, slug):
    games_played = Match.objects.filter(league__slug=slug).count()
    return HttpResponse(games_played)

def total_players(request, slug):
    total_players = PlayerStats.objects.filter(league__slug=slug).values('player').distinct().count()
    return HttpResponse(total_players)

def total_rent(request, slug):
    total_rent = f'${Match.objects.filter(league__slug=slug).values("played_on__date").distinct().count() * 72}'
    return HttpResponse(total_rent)

def avg_games_per_day(request,slug):
    avg = (Match.objects.filter(league__slug=slug)
        .values('played_on__date')
        .annotate(count=Count('id'))
        .values('played_on__date', 'count')
        .aggregate(Avg('count')).values())
    
    return HttpResponse(round(list(avg)[0],2))


def match_results(request,slug):
 
    results = (Match.objects.filter(league__slug=slug)
        .annotate(row_number=Window(expression=RowNumber(), partition_by=[F('played_on__date')], order_by=F('played_on').asc(),))
        .order_by('-played_on'))
    return render(request, 'dash_components/match-results.html', {'results': results})


def player_rankings(request, slug):
    total_matches = Match.objects.count()
    min_matches = round(total_matches/4)

    current_streak = PlayerStats.objects.filter(player=OuterRef('player__id')).order_by('-pk')

    results = (PlayerStats.objects.filter(league__slug=slug)
            .values('player__name')
            .annotate(
                wins=(Count('result', filter=Q(result='W'))),
                losses=(Count('result', filter=Q(result='L'))),
                total=(Count('result')),
                wl_streak= (Max('w_streak')),
                ll_streak= (Max('l_streak')),
                last_played=(Max('match')),
                w_streak=Max(Subquery(current_streak.values('w_streak')[:1])),
                l_streak=Max(Subquery(current_streak.values('l_streak')[:1])),
         
            )
            .filter(total__gt=min_matches)
            .annotate(
                win_pct = (
                        (Cast('wins', FloatField()) / (Cast('total', FloatField())) * 100)
                    ), 
            )
            .order_by('player__name')
            .order_by('-total')
            .order_by('-win_pct')
  
        )

    return render(request, 'dash_components/player-rankings.html', 
        {
            'results': results, 
            'total_matches': total_matches,
            'min_matches': min_matches,
        })


def most_games_played(request, slug):
    games_played = Match.objects.filter(league__slug=slug).count()
    results = (PlayerStats.objects.filter(league__slug=slug)
            .values('player__name')
            .annotate(
                total=(Count('result')),
                pct=(Cast('total', FloatField()) / Cast(games_played, FloatField())*100)
            )
            .order_by('player__name')
            .order_by('-total')
        )

    return render(request, 'dash_components/most-games-played.html', {'results': results})

def rent_breakdown(request, slug):
    results = (
            PlayerStats.objects.filter(league__slug=slug)
             
            .annotate(
                date=Cast('match__played_on', DateField()),
                player_played=F('player__name')
            )
             
        )
    print(results.query)
    #for r in results:
        #print(f'{r}')
    return render(request, 'dash_components/rent-breakdown.html', {'results': results})