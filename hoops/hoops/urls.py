from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main' ),
    path('contact', views.contact, name='contact'),
    path('dashboard/<slug:slug>',views.dashboard, name="dashboard"),

    # dashboard stuff
    path('dashboard/<slug:slug>/games-played',views.games_played),
    path('dashboard/<slug:slug>/total-players',views.total_players),
    path('dashboard/<slug:slug>/total-rent',views.total_rent),
    path('dashboard/<slug:slug>/avg-games-per-day',views.avg_games_per_day),
    path('dashboard/<slug:slug>/match-results',views.match_results),
    path('dashboard/<slug:slug>/player-rankings',views.player_rankings),
    path('dashboard/<slug:slug>/winning-streaks',views.winning_streaks),
    
    
]
