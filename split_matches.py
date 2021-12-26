import pandas as pd
import json

log = open(r'console.log')
last = (0, 'inicio')
start_list = list()
end_list = list()


for lineno, line in enumerate(log):
    if 'get5_event:' in line:

        data = line.split(' get5_event: ')[1]
        data = json.loads(data)
        curr = data['event']
        if curr in ['series_start',
                    # 'going_live',
                    # 'round_end',
                    'map_end',
                    'series_end']:
            if last[1] == 'inicio' and curr == 'series_start':
                start_list.append(lineno)
            # elif last[1] == 'series_start' and curr == 'series_start':
            #     end_list.append(lineno - 1)
            elif last[1] == 'map_end' and curr == 'series_start':
                end_list.append(last[0])
                start_list.append(lineno)
            elif last[1] != 'series_end' and curr == 'series_start':
                end_list.append(lineno - 1)
                start_list.append(lineno)
            elif last[1] == 'series_end' and curr == 'series_start':
                start_list.append(lineno)
            elif curr == 'series_end':
                end_list.append(lineno+1)
            print(lineno, data)

            last = (lineno, curr)

print(start_list)
print(end_list)

log = open(r'console.log')
full = log.readlines()
log.close()

if len(start_list) == len(end_list):
    for i in range(len(start_list)):
        match = full[start_list[i]: end_list[i]]

        data = match[0].split(' get5_event: ')[1]

        data = json.loads(data)
        match_id = data['matchid`']
        horario = match[0][2:20].replace('/', '-')
        horario = horario.replace(' - ', ' ')
        horario = horario.replace(':', '-')

        data2 = data
        try:
            data2 = json.loads(match[-1].split(' get5_event: ')[1])
        except IndexError:
            pass

        x = ''
        if data['event'] == 'series_start' and data2['event'] == 'series_end':
            x = ' full_match'

        if data['event'] == 'series_start' and \
                (data2['event'] == 'series_end' or
                 data2['event'] == 'map_end'):
            f = open(f'matches\\{i} - {horario} - {match_id}{x}.log', 'w')
            f.writelines(match)







