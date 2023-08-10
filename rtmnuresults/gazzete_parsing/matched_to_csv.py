import json

DATA = json.load(open("matched-etc.json"))

with open("data-etc.csv", "w") as f:
    for dp in DATA:
        f.write(f"{dp[0]},{dp[1]},{dp[2]}\n")