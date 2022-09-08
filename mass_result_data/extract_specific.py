import json
import pathlib
import csv


current_dir = pathlib.Path(__file__).parent.absolute()

LINES = []

HEADERS = ['seat_number', 'name', 'branch']
_HEADERS = ['result','total_marks', 'sgpa']

with open(str(current_dir /'data.fmt')) as f:
    for line in f:
        if 'GOVERNMENT COLLEGE OF ENGINEERING, NAGPUR' in line:
            LINES.append(line)

# we take first line and then extract the headers
cur_line = LINES[0]
[seat, name, spga, _data] = line.split('::')
data = json.loads(_data)
for subject in data['result']:
        if subject['assessment_method'].lower() == 'theory':
            HEADERS.append(subject.get('abbreviation') + '-' + 'TU')
            HEADERS.append(subject.get('abbreviation') + '-' + 'TI')
            HEADERS.append(subject.get('abbreviation') + '-' + 'T')
        else:
            HEADERS.append(subject.get('abbreviation') + '-' + 'PU')
            HEADERS.append(subject.get('abbreviation') + '-' + 'PI')
            HEADERS.append(subject.get('abbreviation') + '-' + 'P')

HEADERS += _HEADERS

def transform_data(inp: dict) -> dict:
    out = {}
    for subject in inp['result']:
        if subject['assessment_method'].lower() == 'theory':
            
            out[subject['abbreviation'] + '-' + 'TU'] = subject['university_assessment']['marks_obtained']
            out[subject['abbreviation'] + '-' + 'TI'] = subject['college_assessment']['marks_obtained']
            out[subject['abbreviation'] + '-' + 'T'] = subject['total']['marks_obtained']
        else:
            out[subject['abbreviation'] + '-' + 'PU'] = subject['university_assessment']['marks_obtained']
            out[subject['abbreviation'] + '-' + 'PI'] = subject['college_assessment']['marks_obtained']
            out[subject['abbreviation'] + '-' + 'P'] = subject['total']['marks_obtained']
    out['seat_number'] = int(inp['roll_number'])
    out['name'] = inp['name']
    branch = 'undef'
    if out['seat_number'] > 601242:
        branch = 'Civil'
    if out['seat_number'] > 603981:
        branch = 'Computer'
    if out['seat_number'] > 606013:
        branch = 'Electrical'
    if out['seat_number'] > 607862:
        branch = 'Electronics'
    if out['seat_number'] > 611051:
        branch = 'Mechanical'
    
    out['branch'] = branch
    
    out['total_marks'] = inp['summary']['total_marks_obtained']
    out['result'] = inp['summary']['result']
    out['sgpa'] = inp['summary']['sgpa']
    return out


with open(str(current_dir / 'data.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=HEADERS)
    writer.writeheader()
    for line in LINES:
        [seat, name, spga, _data] = line.split('::')
        data = json.loads(_data)
        writer.writerow(transform_data(data))

