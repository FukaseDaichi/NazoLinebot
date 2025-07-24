import json

with open("./lib/config.json", "r", encoding="utf-8") as f:
    GAME_DATA = json.load(f)["games"]
