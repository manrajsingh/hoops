from hoops import models


def reset_all_player_stats():
    matches = models.Match.objects.all()
    models.PlayerStats.objects.all().delete()

    PlayerStats_instances = []
    for m in matches:

        for p in m.host.all():
            result = 'W' if m.host_score > m.guest_score else 'L'
            PlayerStats_instances.append(models.PlayerStats(
                league=m.league,
                player=p,
                match = m,
                played_as = 'H',
                result=result
            ))

        for p in m.guest.all():
            result = 'W' if m.guest_score > m.host_score else 'L'
            PlayerStats_instances.append(models.PlayerStats(
                league=m.league,
                player=p,
                match = m,
                played_as = 'G',
                result=result
            ))
    #print(PlayerStats_instances)
    models.PlayerStats.objects.bulk_create(PlayerStats_instances)

reset_all_player_stats()