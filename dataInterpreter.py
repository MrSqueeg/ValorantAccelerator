import os
import json
import time

import main

directory = os.path.join(os.path.dirname(__file__), "data")

def main():
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.endswith(".json"):
                f = open(f"{directory}\{file}", 'r')
                print(f"Contents?: {f.read()}")

                # Call AI Function
    else:
        print("Directory Does not exist... Adding Folders...")
        os.makedirs(directory)


if __name__ == "__main__":
    main()