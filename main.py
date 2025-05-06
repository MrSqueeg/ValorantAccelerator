import os
import json
import time
import re

# Make names more descriptive
import get
import averager

from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("KEY")

def main():
    # Filler test values
    region = "na"
    name = "mrsqueeg"
    tag = "3225"
    platform = "pc"
    size = 25
    mode = 'competitive'
    params = {"size": {size}, "mode": {mode}}
    leaderboard = f'https://api.henrikdev.xyz/valorant/v3/leaderboard/{region}/{platform}'

    data = get.retrieve(leaderboard, KEY, params)

    if data != 0:
        print("Got Leaderboard")
        data = data['data']
        players = data['players']

        print("Going through players")
        for player in players:
            userName = player['name']
            userTag = player['tag']
            print(f"{userName}#{userTag}....")
            url = f'https://api.henrikdev.xyz/valorant/v4/matches/{region}/{platform}/{userName}/{userTag}'

            stats = get.retrieve(url, KEY, params)

            if stats != 0:
                print(f'Success!')
                stats = stats['data']
                output_data(averager.get_match_data(stats, userName), 'stats.json')
            else:
                print("Failed to recieve information")

    averager.average_data('stats.json')

    data = get.retrieve(f'https://api.henrikdev.xyz/valorant/v4/matches/{region}/{platform}/{name}/{tag}', KEY, params)
    if data != 0:
        data = data['data']
        print(f"Saving data : {name}")
        get.save(averager.get_match_data(data, name), 'user_stats.json')
        # Get match data and compare


def output_data(json_data, path):
    print(f'Saving player data {json_data['name']}...')
    data = {}
    key = 'players'

    try:
        if not os.path.exists(path):
            pass
        elif os.path.getsize(path) == 0:
            with open(path, 'r') as outfile:    
                json.dump({}, outfile)
        else:
            with open(path, 'r') as outfile:    
                data = json.load(outfile)

        if key not in data:
            print("Key does not exist adding key.....")
            data[key] = []

        
        with open(path, 'w') as outfile: 
            data[key].append(json_data)
            json.dump(data, outfile, indent=4)

    except Exception as e:
        print(json_data)
        print(e)

if __name__ == "__main__":
    main()
