import re
import json
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()

REGEX_PATTERN = r"\d\d\d\d\d\d\(\d\.\d\d\)"


with open(str(CURRENT_DIR / 'data.fmt')) as f:
    DATA = f.read()
    
REGEX = re.compile(REGEX_PATTERN, re.MULTILINE)

FILTERED_DATA = []
UNFILTERED_DATA = []
for match in REGEX.finditer(DATA):
    roll_number, sgpa = match.group().replace(')', "").split('(')
    # print(roll_number, sgpa)
    roll_number = int(roll_number)
    
    if roll_number >= 151384 and roll_number <= 151460:
        FILTERED_DATA.append((roll_number, float(sgpa)))
    UNFILTERED_DATA.append((roll_number, float(sgpa)))

for i in range(151384, 151461):
    if i not in [x[0] for x in FILTERED_DATA]:
        FILTERED_DATA.append((i, 0.0))

FILTERED_DATA.sort(key=lambda x: -x[1])
UNFILTERED_DATA.sort(key=lambda x: -x[1])

json.dump(FILTERED_DATA, open(str(CURRENT_DIR / 'data.json'), 'w'))

with open(str(CURRENT_DIR / 'data2.fmt'), 'w') as f:
    for dp in FILTERED_DATA:
        f.write(f'{dp[0]} {dp[1]}\n')
        
for i in range(0, 10):
    print(f"{i+1}. {UNFILTERED_DATA[i][0]} {UNFILTERED_DATA[i][1]}")