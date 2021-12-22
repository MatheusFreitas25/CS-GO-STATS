import pandas as pd
import json

log = open(r'C:\Users\Matheus F\PycharmProjects\CS-GO-STATS\console.log')

lines = list()

player_events = ['attacked', 'threw flashbang', 'blinded', 'killed', 'left buyzone', 'say_team', 'say', 'threw molotov',
                  'threw hegrenade', 'threw smokegrenade', 'purchased', 'Dropped_The_Bomb', 'Got_The_Bomb',
                  'switched from team', 'assisted killing', 'Planted_The_Bomb', 'Bomb_Begin_Plant', 'flash-assisted killing',
                  'Begin_Bomb_Defuse_With_Kit', 'Defused_The_Bomb', 'entered the game', 'disconnected',
                  'threw decoy', 'Begin_Bomb_Defuse_Without_Kit']

map_events = ['Molotov projectile spawned', 'MatchStatus', 'get5_event:']

row_to_insert = 0

df = pd.DataFrame(columns=player_events)

for line in log:
    lines.append(line.rstrip())

for values_index in range(len(player_events)):
    row_to_insert = 0
    for line in lines:
        if player_events[values_index] in line:
            row_to_insert += 1
            df.loc[row_to_insert, player_events[values_index]] = line

df.to_csv(r'C:\Users\Matheus F\Desktop\export_dataframe.csv', sep=";", index=False, header=True)
