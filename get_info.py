from event import Event
from utils import insert_to_database
import pandas as pd
import json
from os import listdir
from os.path import isfile, join


folder = r'matches'
# file = folder + r'\1 - 12-25-2021 19-12 - bo3 full_match.log'

onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

for file in onlyfiles:

    log = open(folder + '\\' + file)

    events = list()

    moment = 'pre_series'
    mapnumber = 0
    round = 0
    map_name = 'undefined'
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
                match_id = file.split('.')[0]

            elif curr == 'going_live':
                moment = 'warmup'
                mapnumber += 1
                round = 0
                map_name = data['params']['map_name']
                match_id = file.split('.')[0]

            elif curr == 'knife_start':
                moment = 'knife'
                round = 0
                map_name = data['params']['map_name']
                match_id = file.split('.')[0]

            elif curr == 'round_end':
                moment = 'round_ended'

            elif curr == 'map_end':
                moment = 'map_ended'
                round = 0

        elif 'Starting Freeze period' in line:
            moment = 'freeze_time'
            round += 1
        elif 'RoundsPlayed: -1' in line:
            moment = 'warmup'
            round = 0
        elif 'RoundsPlayed: 0' in line:
            if moment == 'warmup':
                moment = 'live'
                round = 1
        elif 'World triggered "Round_Start"' in line:
            if moment == 'freeze_time':
                moment = 'live'
        else:
            event = Event(line, lineno, moment, mapnumber, round, map_name, match_id)
            events.append(event.to_dict())

    df = pd.DataFrame()

    df = df.append(events, ignore_index=True, sort=False)

    df = df[['lineno', 'time', 'moment', 'mapnumber', 'round', 'map_name', 'match_id', 'type', 'author_name', 'author_id',
             'author_side', 'victim_id', 'victim_name', 'victim_side', 'weapon', 'damage', 'blinded_time', 'flashbang_id',
             'damage_armor', 'victim_health', 'victim_armor', 'hitgroup', 'hs', 'penetrated', 'throughsmoke',
             'author_coord', 'victim_coord', 'equipment', 'item_bought']]

    print(df)

    insert_to_database(df)

