import os
import json
import time
import re
#import main

directory = os.path.join(os.path.dirname(__file__), "data")

def main():
    # Look for proper user file
    if os.path.exists(directory):
        for file in os.listdir(directory):
            data = []
            if file.endswith(".json"):
                f = open(f"{directory}\\{file}", 'r')
                print(file)
                data = json.load(f)

                for i in data:
                    print(i)

                # Save user data locally
                currentRank = re.sub(r'[^\d.]+', '', data[0].get('currentRank', ''))
                gamesPlayed = re.sub(r'[^\d.]+', '', data[0].get('gamesPlayed', ''))
                winRate = re.sub(r'[^\d.]+', '', data[0].get('winRate', ''))
                hsPercent = re.sub(r'[^\d.]+', '', data[0].get('hsPercent', ''))
                trackerScore = data[0].get('trackerScore', '')[:data[0].get('trackerScore', '').find(' ')]
                print(trackerScore)
                kast = re.sub(r'[^\d.]+', '', data[0].get('kast', ''))
                acs = re.sub(r'[^\d.]+', '', data[0].get('acs', ''))
                kdRatio = re.sub(r'[^\d.]+', '', data[0].get('kdRatio', ''))
                kadRatio = re.sub(r'[^\d.]+', '', data[0].get('kadRatio', ''))
                killsPerRound = re.sub(r'[^\d.]+', '', data[0].get('killsPerRound', ''))
                roundWinPercent = re.sub(r'[^\d.]+', '', data[0].get('roundWinPercent', ''))
                damagePerRound = re.sub(r'[^\d.]+', '', data[0].get('damagePerRound', ''))

                # Call AI Function Here
    else:
        print("Directory Does not exist... Adding Folders...")
        os.makedirs(directory)


if __name__ == "__main__":
    main()