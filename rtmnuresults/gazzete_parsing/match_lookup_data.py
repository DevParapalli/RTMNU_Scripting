import json

DATA = json.load(open("data-etc.json"))
LOOKUP = json.load(open("lookup-etc.json"))

MATCHED = []
for dp in DATA:
    seat_num, sgpa = dp
    MATCHED.append((seat_num, LOOKUP[str(seat_num)], sgpa))

MATCHED.sort(key=lambda x: -x[2])

json.dump(MATCHED, open("matched-etc.json", "w"))