# Provided a results json with seat numbers, this will extract all the data from it.

import pathlib
import json
from extract import init, extract_html_from_seat_numbers, cleanup, convert
from base64 import b64encode

current_dir = pathlib.Path(__file__).parent.absolute()

#result.json's keys are the seat nums

results = json.loads((current_dir / 'result.json').read_text()).keys()

driver = init()

# The data will be stored incrementally in a massive json file, so that if the program crashes, it can be resumed.
state: list[str | int] = json.loads((current_dir / 'state.json').read_text())

seats_to_check = []
for seat in results:
    if seat not in state:
        seats_to_check.append(seat)
    elif seat in state and not state[seat]:
        seats_to_check.append(seat)


counter = 0
with open(str(current_dir / 'data.fmt'), 'a') as f:
    for html, id in extract_html_from_seat_numbers(driver, seats_to_check):
        if html is None or id is None or id == 000000:
            # The seat number was not found or we do not want to process it.
            continue
        try:
            data = convert(html)
            state[id] = True
            f.write(f"{id}:{b64encode(json.dumps(data).encode()).decode()}")
            counter += 1
            print(f'{counter} / {len(seats_to_check)} | {id}')
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                statement = input('Waiting for input (q to quit)...')
                if statement in ['q', 'Q']:
                    break
            print(e)
            input(f'Check Error...')
            state[id] = False
            continue

# sync state with file
(current_dir / 'state.json').write_text(json.dumps(state))

cleanup(driver)

print(f"Done! Processed {counter} seat numbers.")

# data.append(convert(html))




