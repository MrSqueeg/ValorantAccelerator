from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException

import os
import json
import time
import re

options = ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(use_subprocess=True, options=options)


def scrapeSite(url):
    driver.get(f"{url}")
    time.sleep(5)
    
    print("\nWaiting Done\n")

    # Find cloudflare Decline -- Detects properly, doesnt reset
    try :
        while driver.find_element(By.CSS_SELECTOR, "body.no-js") != None:
            print("\nCloudflare Detected refreshing...\n")
            driver.get("https://www.google.com")
            time.sleep(3)
            driver.get(url)
    except NoSuchElementException:
        print("No Cloud Flare")
        return
    return

def main():
    print("\nProgram Started\n")

    # Get leaderboard players
    urlInfo = "https://www.tracker.gg/valorant/leaderboards/ranked/all/"
    scrapeSite(urlInfo)
    driver.refresh()
    driver.implicitly_wait(4)
    time.sleep(4)

    # Get player tracker link
    print(f"\nLooking for Users on Leaderboard\n")
    usernames = driver.find_elements(By.CSS_SELECTOR,"#app > div.trn-wrapper > div.trn-container > div > main > div.leaderboards > div.content.mt-4 > div > div > div.board > div.trn-table__container > table > tbody > tr > td.username > div > a")

    # Save leaderboard players to file incase lost or move this function to seperate file
    f = open('topPlayers.txt', 'w')
    for user in usernames:
        user = user.get_attribute('href')
        if (user != None):
            print(f"Checking: {user}")
            if ("/valorant/profile" in user):
                f.write(f"{user}\n")
                print("Added to File")

    print("\n\nLeaderboard file Edited...\n\n")
    f.close()

    print("\nScrapping Profiles\n")
    time.sleep(5)
    f = open('topPlayers.txt', 'r')
    Lines = f.readlines()

    # Remove old player profiles
    # - Doing this so if someone falls out of range their old rank doesnt stay in the data set
    directory = os.path.join(os.path.dirname(__file__), "data")
    for file in os.listdir(directory):
        file_path = os.path.join(os.path.dirname(__file__), "data", file)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)


    # Find individual Player Data
    i = 0
    for line in Lines:
        if ("valorant" in line):
            print("Scraping Player...")
            urlInfo = line
            scrapeSite(urlInfo)
            time.sleep(3)

            # Find all data Elements
            username = driver.find_element(By.CSS_SELECTOR, 'span.trn-ign__username').text
            print(username, i)

            currentRank = driver.find_element(By.CSS_SELECTOR, 'div.rating-entry__rank-info div.value').text
            gamesPlayed = driver.find_element(By.CSS_SELECTOR, 'div.title-stats > span.matches').text
            winRate = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="Win %"] + span[class="flex items-center gap-2"] > span.value').text
            trackerScore = driver.find_element(By.CSS_SELECTOR, 'div.performance-score__container div.value').text
            kast = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="KAST"] + span[class="flex items-center gap-2"] > span.value').text
            dDelta = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="DDΔ/Round"] + span[class="flex items-center gap-2"] > span.value').text
            acs = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="ACS"] + span[class="flex items-center gap-2"] > span.value').text
            kdRatio = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="K/D Ratio"] + span[class="flex items-center gap-2"] > span.value').text
            kadRatio = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="KAD Ratio"] + span[class="flex items-center gap-2"] > span.value').text
            killsPerRound = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="Kills/Round"] + span[class="flex items-center gap-2"] > span.value').text
            hsPercent = driver.find_element(By.CSS_SELECTOR, 'div.giant-stats > div:nth-child(3) > div > div.numbers > span.flex.items-center.gap-2 > span').text
            roundWinPercent = driver.find_element(By.CSS_SELECTOR, 'div.performance-score__stats > div[class*="stat stat--tier"] div.stat__value').text
            damagePerRound = driver.find_element(By.CSS_SELECTOR, 'div.giant-stats > div:nth-child(1) > div > div.numbers > span.flex.items-center.gap-2 > span').text

            print("\n\nFinished getting Data\n\n")

            data = []
            data_json = {
                'currentRank' : currentRank,
                'gamesPlayed' : gamesPlayed,
                'winRate' : winRate,
                'trackerScore' : trackerScore,
                'hsPercent' : hsPercent,
                #'Bodyshot Rate' : bsPercent, (Working on these)
                #'Legshot Rate' : lsPercent,
                'kdRatio' : kdRatio,
                'kast' : kast,
                'dDelta' : dDelta,
                'acs' : acs,
                'kadRatio' : kadRatio,
                'killsPerRound' : killsPerRound,
                'roundWinPercent' : roundWinPercent,
                'damagePerRound' : damagePerRound,
            }

            # Create player Json Files
            username = re.sub(r'\s+', '', username)

            if os.path.isfile(f"ValorantAccelerator/data/{username}.json"):
                os.remove(f"ValorantAccelerator/data/{username}.json")
            data.append(data_json)
            f2 = open(f'data/{username}.json', 'w')
            json.dump(data, f2)

            print(f"\n{username}.json Edited/Created\n")
        i += 1

    print("\nAll Users scrapped!\n")   
    driver.implicitly_wait(5)
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        if e.args[0] == 6:
            driver.quit()
            print(f"\nDriver Quit due to Error: {e}\n")
