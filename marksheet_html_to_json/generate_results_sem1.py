import json
import glob
import csv
import pathlib

current_directory = pathlib.Path(__file__).parent.absolute()

HEADERS = ['seat_number', 'name', 'branch']

_HEADERS = ['result','total_marks', 'sgpa']

all_marksheets = glob.glob(str(current_directory / 'json' / '*.json'))

with open(all_marksheets[0]) as f:
    data = json.load(f)
    for subject in data['result']:
        if subject['assessment_method'].lower() == 'theory':
            HEADERS.append(subject.get('abbreviation') + '-' + 'TU')
            HEADERS.append(subject.get('abbreviation') + '-' + 'TI')
            HEADERS.append(subject.get('abbreviation') + '-' + 'T')
        else:
            HEADERS.append(subject.get('abbreviation') + '-' + 'PU')
            HEADERS.append(subject.get('abbreviation') + '-' + 'PI')
            HEADERS.append(subject.get('abbreviation') + '-' + 'P')

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

with open(str(current_directory / 'results.csv'), "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=HEADERS + _HEADERS)
    writer.writeheader()
    for marksheet in all_marksheets:
        with open(marksheet) as f:
            data = json.load(f)
            writer.writerow(transform_data(data))