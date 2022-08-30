import json
import pathlib
import csv

current_dir = pathlib.Path(__file__).parent.absolute()

COLUMNS = ["seat", "branch", "name", "marks", "sgpa"]

with open(str(current_dir / 'result.json'), 'r') as f:
    RESULT = json.load(f)

with open(str(current_dir / 'hall_ticket.json'), 'r') as f:
    HALL_TICKET = json.load(f)

DATA = []

for key, value in HALL_TICKET.items():
    # Some keys are not in result
    if key in RESULT:
        DATA.append([
            key,
            value['branch'],
            value['name'],
            RESULT[key]['marks'],
            RESULT[key]['sgpa']
        ])
    else:
        DATA.append([
            key,
            value['branch'],
            value['name'],
            0,
            0
        ])

DATA.sort(key=lambda x: x[4], reverse=True)

with open(str(current_dir / 'merged.csv'), 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(COLUMNS)
    writer.writerows(DATA)


with open(str(current_dir / 'merged.json'), 'w') as f:
    json.dump(DATA, f)


