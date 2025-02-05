import time
import csv
import json
import requests
import os
import averager

def retrieve(url, API_KEY):
    headers = {
        'Authorization': API_KEY,
        'User-Agent': 'Valorant Accelerator'
    }

    try:
        response = requests.get(url=url, headers=headers)
        print(response.text)

        data = json.loads(response.text)['data']
        return data

    except requests.exceptions.RequestException as e:
        print(f'Error while requesting api: {e}')

def save(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(str(data))