import math
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from hoops import models

 
@receiver(m2m_changed, sender=models.Match.host.through)
def create_remove_host_player_stats(sender, instance, action, **kwargs):
    result = 'W' if instance.host_score > instance.guest_score else 'L'
    create_remove_player_stats(instance, action, instance.host.all(),"H", result)


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
                PlayerStats_instances.append(
                    models.PlayerStats(
                        league=instance.league,
                        player=p,
                        match = instance,
                        played_as = team_type,
                        result=result
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
            PlayerStats_instances.append(
                models.PlayerStats(
                        league=instance.league,
                        player=p,
                        match = instance,
                        played_as = team_type,
                        result=result
                    )
                )
        q = models.PlayerStats.objects.bulk_create(PlayerStats_instances)
        

@receiver(post_save, sender=models.Match)
def update_player_stats(sender, instance, created, **kwargs):
    
    if not created:
        PlayerStats_instances = []

        for p in instance.host.all():
            result = 'W' if instance.host_score > instance.guest_score else 'L'
            match_instance = models.PlayerStats.objects.get(
                    league=instance.league,
                    player=p,
                    match = instance
                )
            match_instance.result = result
            PlayerStats_instances.append(match_instance)

        for p in instance.guest.all():
            result = 'W' if instance.guest_score > instance.host_score else 'L'
            match_instance = models.PlayerStats.objects.get(
                    league=instance.league,
                    player=p,
                    match = instance
                )
            match_instance.result = result
            PlayerStats_instances.append(match_instance)
        models.PlayerStats.objects.bulk_update(PlayerStats_instances, 
            (field.name for field in models.PlayerStats._meta.get_fields() if not field.name in ('id'))
        )
        

@receiver(post_delete, sender=models.Match)
def delete_player_stats(sender, instance, **kwargs):
    models.PlayerStats.objects.filter(match=instance).delete()