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
    name = "MrSqueeg"
    tag = "3225"
    platform = "pc"
    size = 4
    mode = 'unrated'
    params = {"size": {size}, "mode": {mode}}
    url = f'https://api.henrikdev.xyz/valorant/v4/matches/{region}/{platform}/{name}/{tag}'

    print(url)


    data = get.retrieve(url, KEY, params)

    if data != 0:
        data = data['data']
        get.save(data, "matches.json")
        averager.get_match_data(data, name)

if __name__ == "__main__":
    main()
