from event import Event
from utils import insert_to_database
import pandas as pd
import json


log = open(r'matches\5 - 12-21-2021 19-34 - bo3 full_match.log')

events = list()

moment = 'pre_series'
mapnumber = 0
round = 0
map_name = 'undefined'
match_id = '0'
dead_t = 0
dead_ct = 0

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
            moment = 'warmup'
            mapnumber += 1
            round = 0
            map_name = data['params']['map_name']
            match_id = data['matchid`']

        elif curr == 'round_end':
            moment = 'round_ended'

        elif curr == 'map_end':
            moment = 'map_ended'
            round = 0

    elif 'Starting Freeze period' in line:
        moment = 'freeze_time'
        round += 1
        dead_ct = 0
        dead_t = 0
    elif 'World triggered "Match_Start"' in line:
        moment = 'warmup'
        round = 0
    elif 'World triggered "Round_Start"' in line:
        if moment == 'freeze_time':
            moment = 'live'
    else:
        event = Event(line, lineno, moment, mapnumber, round, map_name, match_id)
        if event.type == 'killed' and event.victim_side == 'CT':
            dead_ct += 1
        if event.type == 'killed' and event.victim_side == 'TERRORIST':
            dead_t += 1
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

df = df.append(events, ignore_index=True, sort=False)

df = df[['lineno', 'time', 'moment', 'mapnumber', 'round', 'map_name', 'match_id', 'type', 'author_name', 'author_id',
         'author_side', 'victim_id', 'victim_name', 'victim_side', 'weapon', 'damage', 'blinded_time', 'flashbang_id',
         'damage_armor', 'victim_health', 'victim_armor', 'hitgroup', 'hs', 'penetrated', 'throughsmoke',
         'author_coord', 'victim_coord']]


insert_to_database(df)

# df[~pd.isna(df['type'])].to_csv('eventos.csv', index=False, sep=';')


