import math
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from hoops import models


def get_streak(player, current_result):
        last_entry = models.PlayerStats.objects.filter(player=player).order_by('-match__played_on').first()
        if last_entry is None:
            if current_result == 'W':
                return {'ws':1, 'ls': 0}
            else:
                return {'ws':0, 'ls': 1}
        else:
            if current_result == 'W':
                if last_entry.result == 'W':
                    return {'ws':last_entry.w_streak + 1, 'ls': 0}
                else:
                    return {'ws':1, 'ls': 0}
            else:
                if last_entry.result == 'W':
                    return {'ws':0, 'ls': 1}
                else:
                    return {'ws':0, 'ls': last_entry.l_streak + 1}


# Triggered when host player is changed / removed 
@receiver(m2m_changed, sender=models.Match.host.through)
def create_remove_host_player_stats(sender, instance, action, **kwargs):
    result = 'W' if instance.host_score > instance.guest_score else 'L'
    create_remove_player_stats(instance, action, instance.host.all(),"H", result)


# Triggered when guest player is changed / removed 
@receiver(m2m_changed, sender=models.Match.guest.through)
def create_remove_guest_player_stats(sender, instance, action, **kwargs):
    result = 'W' if instance.guest_score > instance.host_score else 'L'
    create_remove_player_stats(instance, action, instance.guest.all(), "G", result)


def create_remove_player_stats(instance, action, players, team_type, result):
    
    if action == "post_add":
        PlayerStats_instances = []
        for p in players:
            match_instance = models.PlayerStats.objects.filter(
                    league=instance.league,
                    player=p,
                    match = instance
                ).first()
            if match_instance is not None:
                match_instance.played_as = team_type
                match_instance.result = result
                match_instance.save()
            else:
                streak = get_streak(p, result)
                PlayerStats_instances.append(
                    models.PlayerStats(
                        league=instance.league,
                        player=p,
                        match = instance,
                        played_as = team_type,
                        result=result,
                        w_streak = streak['ws'],
                        l_streak = streak['ls'],
                    )
                )
        q = models.PlayerStats.objects.bulk_create(PlayerStats_instances)

    elif action == "post_remove":
        models.PlayerStats.objects.filter(
            league=instance.league,
            match = instance,
            played_as = team_type
        ).delete()

        PlayerStats_instances = []
        for p in players:
            streak = get_streak(p, result)
            PlayerStats_instances.append(
                models.PlayerStats(
                        league=instance.league,
                        player=p,
                        match = instance,
                        played_as = team_type,
                        result=result,
                        w_streak = streak['ws'],
                        l_streak = streak['ls'],
                    )
                )
        q = models.PlayerStats.objects.bulk_create(PlayerStats_instances)
        


# Triggerd when scores or anything else other than host / guest team is updated
@receiver(post_save, sender=models.Match)
def update_player_stats(sender, instance, created, **kwargs):
    
    if not created:
        PlayerStats_instances = []

        for p in instance.host.all():
            result = 'W' if instance.host_score > instance.guest_score else 'L'
            streak = get_streak(p, result)
            match_instance = models.PlayerStats.objects.get(
                    league=instance.league,
                    player=p,
                    match = instance
                )
            match_instance.result = result
            match_instance.w_streak = streak['ws']
            match_instance.l_streak = streak['ls']
            PlayerStats_instances.append(match_instance)

        for p in instance.guest.all():
            result = 'W' if instance.guest_score > instance.host_score else 'L'
            streak = get_streak(p, result)
            match_instance = models.PlayerStats.objects.get(
                    league=instance.league,
                    player=p,
                    match = instance
                )
            match_instance.result = result
            match_instance.w_streak = streak['ws']
            match_instance.l_streak = streak['ls']
            PlayerStats_instances.append(match_instance)
        models.PlayerStats.objects.bulk_update(PlayerStats_instances, 
            (field.name for field in models.PlayerStats._meta.get_fields() if not field.name in ('id'))
        )
        
# Triggered when Match is removed
@receiver(post_delete, sender=models.Match)
def delete_player_stats(sender, instance, **kwargs):
    models.PlayerStats.objects.filter(match=instance).delete()