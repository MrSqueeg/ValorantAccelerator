import os
import json
import re

directory = os.path.join(os.path.dirname(__file__), "data")

def main():
    if not os.path.exists(directory):
        print("Directory does not exist... Adding Folders...")
        os.makedirs(directory)
        return

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            print(filename)
            
            with open(filepath, 'r') as file:
                data = json.load(file)

            if data:
                # Isolate integers (thx Chatgpt)
                fields = ['currentRank', 'gamesPlayed', 'winRate', 'hsPercent',
                          'trackerScore', 'kast', 'acs', 'kdRatio', 'kadRatio',
                          'killsPerRound', 'roundWinPercent', 'damagePerRound']

                isolatedData = {}
                for field in fields:
                    if field == "trackerScore":
                        isolatedData[field] = data[0].get(field, '')[:data[0].get(field, '').find(' ')]
                    else:
                        isolatedData[field] = re.sub(r'[^\d.]+', '', data[0].get(field, ''))

                print(isolatedData)

if __name__ == "__main__":
    main()
