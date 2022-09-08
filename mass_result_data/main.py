# Provided a results json with seat numbers, this will extract all the data from it.

import pathlib
import json
from extract import init, extract_html_from_seat_numbers, cleanup, convert_part_result
from base64 import b64encode

current_dir = pathlib.Path(__file__).parent.absolute()

# result.json's keys are the seat nums

results: list[str] = json.loads((current_dir / 'result.json').read_text()).keys()

driver = init()

# The data will be stored incrementally in a massive json file, so that if the program crashes, it can be resumed.
state: list[str | int] = []

with open(str(current_dir / 'state.fmt'), 'r') as f:
    for line in f:
        state.append(line.strip())

seats_to_check = []
for seat in results:
    if (seat not in state and seat not in seats_to_check):
        seats_to_check.append(seat)

seats_to_check = sorted(list(set(seats_to_check)))


counter = 0
with open(str(current_dir / 'data.fmt'), 'a') as f:
    with open(str(current_dir / 'state.fmt'), 'a') as s:
        with open(str(current_dir / 'error.fmt'), 'a') as err:
            for html, id in extract_html_from_seat_numbers(driver, seats_to_check, 0000000):
                if (html is None and id is None) or id == 0000000:
                    # The seat number was not found or we do not want to process it.
                    continue
                if (html is None and id is not None):
                    print('Seat number not found: ' + str(id))
                    err.write(f"{id}\n")
                try:
                    data = convert_part_result(html)
                    f.write(
                        f"{id}::{data['name']}::{data['summary']['sgpa']}::{json.dumps(data)}\n"
                    )
                    counter += 1
                    print(f'{counter} / {len(seats_to_check)} | {id} | {data["name"]}')
                    s.write(f"{id}\n")
                except Exception as e:
                    if isinstance(e, KeyboardInterrupt):
                        statement = input('Waiting for input (q to quit)...')
                        if statement in ['q', 'Q']:
                            break
                    input('ERROR : ' + str(e) + "::" + f"{id}")
                    raise e

# sync state with file
# (current_dir / 'state.json').write_text(json.dumps(state))

cleanup(driver)

print(f"Done! Processed {counter} seat numbers.")

# data.append(convert(html))
