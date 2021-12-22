import pandas as pd
import json

log = open(r'C:\Users\mauro\Desktop\stats mix\\' + 'log\\console.log')

lines = list()

for line in log:
    lines.append(line.rstrip())

get5_events = list()
bang_ids = list()

for line in lines:
    if 'get5_event:' in line:
        data = line.split(' get5_event: ')[1]
        data = json.loads(data)
        # print(data['event'])
        if data['event'] not in get5_events:
            get5_events.append(data['event'])

    # if 'threw flashbang' in line or 'blinded' in line:
    #     item = line.split('entindex ')[1][0:3]
    #     print(line)

    if 'threw flashbang' in line and 'STEAM_1:0:62033627' in line:
        # print(line)
        bang_id = line.split('flashbang entindex ')[1][0:3]
        if bang_id not in bang_ids:
            bang_ids.append(bang_id)

    if len(line.split('<TERRORIST>')) > 1:
        acao = line.split('<TERRORIST>')[1]
        # print(acao)
    elif len(line.split('<CT>')) > 1:
        acao = line.split('<CT>')[1]
        # print(acao)

    eventos_player = ['attacked', 'threw flashbang', 'blinded', 'killed', 'left buyzone', 'say_team', 'say', 'threw molotov',
                      'threw hegrenade', 'threw smokegrenade', 'purchased', 'Dropped_The_Bomb', 'Got_The_Bomb',
                      'switched from team', 'assisted killing', 'Planted_The_Bomb', 'Bomb_Begin_Plant', 'flash-assisted killing',
                      'Begin_Bomb_Defuse_With_Kit', 'Defused_The_Bomb', 'entered the game', 'disconnected',
                      'threw decoy', 'Begin_Bomb_Defuse_Without_Kit']

    eventos_mapa = ['Molotov projectile spawned', 'MatchStatus', 'get5_event:']

    test = 0
    for item in (eventos_player + eventos_mapa):
        if item in line:
            test = 1

    if test == 0:
        print(line)

print(get5_events)
print(bang_ids)


