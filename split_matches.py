import pandas as pd
import json

log = open(r'console.log')
full = log.readlines()
log.close()


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
                    'going_live',
                    # 'round_end',
                    'map_end',
                    'series_end']:

            if last[1] == 'inicio' and curr == 'series_start':
                start_list.append(lineno)
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

if len(start_list) == len(end_list):
    for i in range(len(start_list)):
        match = full[start_list[i]: end_list[i]]
        f = open(f'matches\\{i}.log', 'w')
        f.writelines(match)







