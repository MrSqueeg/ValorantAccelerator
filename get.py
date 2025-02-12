import time
import csv
import json
import requests
import os
import averager

def retrieve(url, API_KEY, params):
    headers = {
        'Authorization': API_KEY,
        'User-Agent': 'Valorant Accelerator'
    }

    try:
        print("Retriving Information...")
        response = requests.get(url=url, headers=headers, params=params)

        # Check if data recieved
        data = json.loads(response.text)
        if data['status'] == 200:
            print("Data reiceved!")
            return data
        
        return 0

    except requests.exceptions.RequestException as e:
        print(f'Error while requesting api: {e}')

def save(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(str(data))