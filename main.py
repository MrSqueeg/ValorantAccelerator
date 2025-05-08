import os
import json
import time
import re
import sys, getopt, optparse


# Make names more descriptive
import get, averager, compare_stats

from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("KEY")

name = 'mrsqueeg'
tag = '3225'
region = 'na'
platform = 'pc'
size = 25
mode = 'competitive'

params = {"size": {size}, "mode": {mode}}
def main():
    # Parse Command line for input
    if parse_command() == 0:
        return
    

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
    print(f"Saving player data {json_data['name']}...")
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

def parse_command():
    global name, tag, region, platform, params
    parser = optparse.OptionParser(usage="Improper Usage")
    parser.add_option('-c', '--compare', action="store_true", dest='compare', \
                      help="Skip getting information and Compare user data (Optional)")
    parser.add_option('-u', '--user', type='string', dest='user', \
                      help="Set username to compare")
    parser.add_option('-t', '--tag', type='string', dest='tag', \
                      help="Set tag for user")
    parser.add_option('-r', '--region', type='string', dest='region', \
                      help="Set region for user (Optional, Default = NA)\nValid Regions: 'na', 'eu', 'latam', 'br', 'ap', 'kr'")
    parser.add_option('-p', '--platform', type='string', dest='platform', \
                      help="Set platform for user (Optional, Default = PC)\nValid Platforms: 'pc', 'console'")
    parser.add_option('-v', dest='verbose', action='store_true')
    (options, args) = parser.parse_args()

    if (options.user == None or options.tag == None):
        print(parser.usage)
        return 0
    else:
        name = options.user
        tag = options.tag

        if options.region != None:
            if options.region.lower in ('na', 'eu', 'latam', 'br', 'ap', 'kr'):
                region = options.region
        else:
            print("Invalid region, using default: NA")

        if options.platform != None:
            if options.platform.lower in ('pc', 'console'):
                platform = options.platform
            else:
                print("Invalid platform, using default: PC")
        
        if options.compare == True:
            data = get.retrieve(f'https://api.henrikdev.xyz/valorant/v4/matches/{region}/{platform}/{name}/{tag}', KEY, params)
            if data != 0:
                data = data['data']
                print(f"Saving data : {name}")
                get.save(averager.get_match_data(data, name), 'user_stats.json')
                compare_stats.compare_stats(user_stats='user_stats.json', average_stats='averaged_stats.json')
                return 0
        
        return 1



if __name__ == "__main__":
    main()
