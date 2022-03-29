from django.shortcuts import render, HttpResponse
from django.db.models import Count, Avg, Window, F, Q, FloatField
from django.db.models.functions import RowNumber, Cast
from . models import League, Match, PlayerStats

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
    results = (PlayerStats.objects.filter(league__slug=slug)
            .values('player__name')
            .annotate(
                wins=(Count('result', filter=Q(result='W'))),
                losses=(Count('result', filter=Q(result='L'))),
                total=(Count('result')),
            )
            .annotate(
                win_pct = (
                        Cast('wins', FloatField()) / (Cast('total', FloatField()))
                    )
            )
            .order_by('-total')
            .order_by('-win_pct')
        )
    return render(request, 'dash_components/player-rankings.html', {'results': results})


def winning_streaks(request, slug):
    results = (PlayerStats.objects.filter(league__slug=slug)
            .values('player__name')
            .annotate(
                wins=(Count('result', filter=Q(result='W'))),
                losses=(Count('result', filter=Q(result='L'))),
                total=(Count('result')),
            )
            .annotate(
                win_pct = (
                        Cast('wins', FloatField()) / (Cast('total', FloatField()))
                    )
            )
            .order_by('-total')
            .order_by('-win_pct')
        )
    return render(request, 'dash_components/player-rankings.html', {'results': results})

def top_teams(request, slug):
    results = (PlayerStats.objects.filter(league__slug=slug)
            .values('player__name')
            .annotate(
                wins=(Count('result', filter=Q(result='W'))),
                losses=(Count('result', filter=Q(result='L'))),
                total=(Count('result')),
            )
            .annotate(
                win_pct = (
                        Cast('wins', FloatField()) / (Cast('total', FloatField()))
                    )
            )
            .order_by('-total')
            .order_by('-win_pct')
        )
    for r in results:
        print(f'{r}')
    return render(request, 'dash_components/player-rankings.html', {'results': results})