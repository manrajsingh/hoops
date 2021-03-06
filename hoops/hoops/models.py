from calendar import c
from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50,null=False, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=50)
    date_added= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']

        
    def __str__(self):
        return self.name
    
    
class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    played_on = models.DateTimeField()
    host = models.ManyToManyField(Player, related_name='host')
    guest= models.ManyToManyField(Player, related_name='guest')
    host_score = models.IntegerField()
    guest_score = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Matches'


    def __str__(self):
        return f"{self.league} {self.played_on}"


class PlayerStats(models.Model):
    result_choices = (
        ('W', 'Won'),
        ('L', 'Lost'),
        ('I', 'In Progress')
    )
    played_as_choices = (
        ('H','Host'),
        ('G', 'Guest')
    )
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match')
    played_as = models.CharField(max_length=1, choices=played_as_choices, default='U')
    result = models.CharField(max_length=1, choices=result_choices, default='I')
    w_streak = models.IntegerField(default=0)
    l_streak = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Player Stats'

    def __str__(self):
        return f"{self.league.name} {self.player.name} {self.match} {self.result}"
