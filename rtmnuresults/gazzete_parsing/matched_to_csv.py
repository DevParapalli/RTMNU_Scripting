import json

DATA = json.load(open("matched.json"))

with open("data.csv", "w") as f:
    for dp in DATA:
        f.write(f"{dp[0]},{dp[1]},{dp[2]}\n")