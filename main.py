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
    url = f'https://api.henrikdev.xyz/valorant/v3/matches/{region}/{name}/{tag}'


    data = get.data(url, KEY)
    get.save(data, "matches.json")

    averager.get_match_data(data, name)

if __name__ == "__main__":
    main()
