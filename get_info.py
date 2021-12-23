from event import Event
import pandas as pd
import json

log = open(r'matches\5 - 12-21-2021 19-34 - bo3 full_match.log')

events = list()

moment = 'pre_series'
mapnumber = 0
round = 0
map_name = ''
match_id = '0'

for lineno, line in enumerate(log):
    if 'get5_event' in line:
        data = line.split(' get5_event: ')[1]
        data = json.loads(data)
        curr = data['event']
        if curr == 'series_start':
            moment = 'map_vetoing'
            mapnumber = 0
            round = 0
            match_id = data['matchid`']

        elif curr == 'going_live':
            moment = 'live'
            mapnumber += 1
            round = 1
            map_name = data['params']['map_name']
            match_id = data['matchid`']

        elif curr == 'round_end':
            moment = 'round_ended'

    elif 'Starting Freeze period' in line:
        moment = 'freeze_time'
        round += 1
    elif 'World triggered "Round_Start"' in line:
        moment = 'live'
    else:
        event = Event(line, lineno, moment, mapnumber, round, map_name, match_id)
        events.append(event.to_dict())

types = list()
player_events = ['attacked', 'threw flashbang', 'blinded', 'killed', 'left buyzone', 'say_team', 'say',
                 'threw molotov', 'committed suicide', 'changed name',
                 'threw hegrenade', 'threw smokegrenade', 'purchased', 'Dropped_The_Bomb', 'Got_The_Bomb',
                 'switched from team', 'assisted killing', 'Planted_The_Bomb', 'Bomb_Begin_Plant',
                 'flash-assisted killing',
                 'Begin_Bomb_Defuse_With_Kit', 'Defused_The_Bomb', 'entered the game', 'disconnected',
                 'threw decoy', 'Begin_Bomb_Defuse_Without_Kit']

df = pd.DataFrame()
for ev in events:
    df = df.append(ev, ignore_index=True)
df[~pd.isna(df['type'])].to_csv('eventos.csv', index=False)


