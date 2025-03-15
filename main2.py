import json

with open("save.json", "r") as file:
    json_data = json.load(file)

players = {}

for player_id, player_name in json_data["playerNames"]["value"].items():
    players[player_id] = player_name

# Save the players dictionary back to the JSON data
json_data["playerNames"]["value"] = players


for player_id, player_name in players.items():
    print(f"ID: {player_id}, Name: {player_name}")

print(players)
