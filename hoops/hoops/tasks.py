
from hoops import models



def reset_all_player_stats():
    matches = models.Match.objects.all()
    models.PlayerStats.objects.all().delete()

    PlayerStats_instances = []
    player_stats={}
    for m in matches:
        for p in m.host.all():
            result = 'W' if m.host_score > m.guest_score else 'L'
            ws=0
            ls=0
            if p.id in player_stats:
                player_stats_count = len(player_stats[p.id])
                if player_stats_count >= 1:
                    last_result = player_stats[p.id][player_stats_count - 1]
                    if result == last_result[:1]:
                        if result == 'W':
                            ws = int(last_result[-1:])+1
                            ls = 0
                        else:
                            ls = int(last_result[-1:])+1
                            ws = 0
                        player_stats[p.id].append(f'{result}-{int(last_result[-1:])+1}')
                    else:
                        if result == 'W':
                            ws = 1
                            ls = 0
                        else:
                            ls = 1
                            ws = 0
                        player_stats[p.id].append(f'{result}-1')
                else:
                    if result == 'W':
                        ws = 1
                        ls = 0
                    else:
                        ls = 1
                        ws = 0
                    player_stats[p.id].append(f'{result}-1')
                    
            else:
                if result == 'W':
                    ws =1
                    ls = 0
                else:
                    ls =1
                    ws = 0
                player_stats[p.id] = [f'{result}-1']

            PlayerStats_instances.append(models.PlayerStats(
                league=m.league,
                player=p,
                match = m,
                played_as = 'H',
                result=result,
                w_streak=ws,
                l_streak=ls
            ))


        for p in m.guest.all():
            result = 'W' if m.guest_score > m.host_score else 'L'
            ws=0
            ls=0
            if p.id in player_stats:
                player_stats_count = len(player_stats[p.id])
                if player_stats_count >= 1:
                    last_result = player_stats[p.id][player_stats_count - 1]
                    if result == last_result[:1]:
                        if result == 'W':
                            ws = int(last_result[-1:])+1
                            ls = 0
                        else:
                            ls = int(last_result[-1:])+1
                            ws = 0
                        player_stats[p.id].append(f'{result}-{int(last_result[-1:])+1}')
                    else:
                        if result == 'W':
                            ws = 1
                            ls = 0
                        else:
                            ls = 1
                            ws = 0
                        player_stats[p.id].append(f'{result}-1')
                else:
                    if result == 'W':
                        ws = 1
                        ls = 0
                    else:
                        ls = 1
                        ws = 0
                    player_stats[p.id].append(f'{result}-1')
            else:
                if result == 'W':
                    ws =1
                    ls = 0
                else:
                    ls =1
                    ws = 0
                player_stats[p.id] = [f'{result}-1']

            PlayerStats_instances.append(models.PlayerStats(
                league=m.league,
                player=p,
                match = m,
                played_as = 'G',
                result=result,
                w_streak=ws,
                l_streak=ls
            ))
 
    models.PlayerStats.objects.bulk_create(PlayerStats_instances)
 
reset_all_player_stats()