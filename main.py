from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException

import os
import json
import time

options = ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=options)

data = []

def scrapeSite(url):
    driver.get(f"{url}")
    time.sleep(4)
    driver.implicitly_wait(4)
    driver.refresh()
    time.sleep(4)
    
    print("\nWaiting Done\n")

    # Find cloudflare Decline -- Detects properly, doesnt reset
    try :
        if driver.find_element(By.CSS_SELECTOR, "body.no-js") != None:
            driver.close()
            print("\nCloudflare Detected refreshing...\n")
            time.sleep(5)
            retrieve_html_page(url)
    except NoSuchElementException:
        return
    return

def main():
    urlInfo = "https://www.tracker.gg/valorant/leaderboards/ranked/all/"
    scrapeSite(urlInfo)

    print(f"\nLooking for Users on Leaderboard\n")

    usernames = driver.find_elements(By.TAG_NAME,"a")

    f = open('topPlayers.txt', 'w')
    for user in usernames:
        user = user.get_attribute('href')
        if (user != None):
            print(f"Checking: {user}")
            if ("/valorant/profile" in user):
                f.write(f"{user}\n")
                print("Added to File")

    print("\n\nFile Edited...\n\n")

    f.close()

    # Find individual Player Data
    f = open('topPlayers.txt', 'r')
    Lines = f.readlines()

    i = 0
    for line in Lines:
        if ("valorant" in line):
            urlInfo = line
            scrapeSite(urlInfo)

            print("\n\nScrapping Profiles\n\n")

            # Find all data Elements
            username = driver.find_element(By.CSS_SELECTOR, 'span.trn-ign__username').text
            currentRank = driver.find_element(By.CSS_SELECTOR, 'div.rating-entry__rank-info div.value').text
            gamesPlayed = driver.find_element(By.CSS_SELECTOR, 'div.title-stats > span.matches').text
            winRate = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="Win %"] + span[class="flex items-center gap-2"] > span.value').text
            trackerScore = driver.find_element(By.CSS_SELECTOR, 'div.performance-score__container div.value ').text
            kast = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="KAST"] + span[class="flex items-center gap-2"] > span.value').text
            dDelta = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="DDΔ/Round"] + span[class="flex items-center gap-2"] > span.value').text
            acs = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="ACS"] + span[class="flex items-center gap-2"] > span.value').text
            kdRatio = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="K/D Ratio"] + span[class="flex items-center gap-2"] > span.value').text
            kadRatio = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="KAD Ratio"] + span[class="flex items-center gap-2"] > span.value').text
            killsPerRound = driver.find_element(By.CSS_SELECTOR, 'div.numbers > span[title*="Kills/Round"] + span[class="flex items-center gap-2"] > span.value').text
            hsPercent = driver.find_element(By.CSS_SELECTOR, 'div.giant-stats > div:nth-child(3) > div > div.numbers > span.flex.items-center.gap-2 > span').text
            roundWinPercent = driver.find_element(By.CSS_SELECTOR, 'div.performance-score__stats > div[class="stat stat--tier-S"] div.stat__value').text
            damagePerRound = driver.find_element(By.CSS_SELECTOR, 'div.giant-stats > div:nth-child(1) > div > div.numbers > span.flex.items-center.gap-2 > span').text

            print("\n\nFinished getting Data\n\n")
            data_json = {
                'Rank RR' : currentRank,
                'Games Played' : gamesPlayed,
                'Winrate' : winRate,
                'Tracker.gg Score' : trackerScore,
                'Headshot Rate' : hsPercent,
                #'Bodyshot Rate' : bsPercent,
                #'Legshot Rate' : lsPercent,
                'KD Ratio' : kdRatio,
                'KAST' : kast,
                'Damage Delta per Round' : dDelta,
                'ACS' : acs,
                'KAD Ratio' : kadRatio,
                'Kills per Round' : killsPerRound,
                'Round Win %' : roundWinPercent,
            }

            print("\n\nstats.json Edited\n\n")

            # Create player Json Files
            if os.path.isfile(f"ValorantAccelerator/data/{username}.json"):
                os.remove(f"ValorantAccelerator/data/{username}.json")
            data.append(data_json)
            f2 = open(f'data/{username}.json', 'w')
            json.dump(data, f2)

        i += 1
        
    driver.quit()



if __name__ == "__main__":
    main()