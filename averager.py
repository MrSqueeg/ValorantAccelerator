import get
import json

fields = [
    "name",
    "winRate",
    "hsPercent",
    "bsPercent",
    "lsPercent",
    "kda",
    "dDelta",
    "acs",
    "kadRatio",
    "killsPerRound",
    "roundWinPercent",
    "damagePerRound"
]

def get_match_data(data, name):
    # Setup values (this is so ugly)
    matches = 0
    kills = 0
    deaths = 0
    kda = 0
    bs = 0
    hs = 0
    ls = 0
    roundsWon = 0
    roundsLost = 0
    dDelta = 0
    acs = 0
    kast = 0
    assists = 0
    damagePerRound = 0
    winRate = 0
    i = 0
    j = 0

    for match in data:
        matches += 1
        team = None
        players = match['players']
        print(f'Match #{matches}, Mode: {match['metadata']['queue']['name']}')
        for player in players:
            j += 1

            # Get player general match statistics
            if player['name'].lower() == name.lower():
                kills += player['stats']['kills']
                deaths += player['stats']['deaths']
                player_team = player['team_id']
                hs += player['stats']['headshots']
                bs += player['stats']['bodyshots']
                ls += player['stats']['legshots']
                dDelta += player['stats']['damage']['dealt'] # NEEDS TO CHANGE TO PER ROUND!
                dDelta -= player['stats']['damage']['received']
                acs += player['stats']['score']
                assists += player['stats']['assists']
                j = 0
                break

        # Get general round stats
        for team in match['teams']:
            if player_team == team['team_id']:
                if team['won'] == True:
                    winRate += 1
                roundsWon += team['rounds']['won']
                roundsLost += team['rounds']['lost']
                break
        
        # Get round stats
        for round in match['rounds']:
            # Calculate players Kast
            for player in round['stats']:
                if player['player']['name'].lower() == name.lower():
                    gotKill = player['stats'].get('kills')
                    gotAssist = player['stats'].get('assists') # For some reason no assist stats are in the data yet are listed in the api documentation
                    
                    survived = 0
                    if player["economy"]['remaining'] == 1:
                        survived = 1

                    if gotKill or gotAssist or survived:
                        kast += 1
    
                    # Get damage dealt in a round not including self
                    if len(player['damage_events']) > 0:
                        for event in player['damage_events']:
                            if event['player']['name'] != name:
                                damagePerRound += event['damage']

    ## Get average statistics

    # Add divide by 0 fix
    roundWinPercent = safe_divide(roundsWon, roundsLost) or 1
    winRate = safe_divide(winRate, matches)
    roundsPlayed = roundsWon + roundsLost
    totalShots = ls + bs + hs
    hsPercent = safe_divide(hs, totalShots) or 1
    bsPercent = safe_divide(bs, totalShots) or 1
    lsPercent = safe_divide(ls, totalShots) or 1
    kda = safe_divide(kills, deaths) or kills
    kadRatio = safe_divide(kills + assists, deaths)
    killsPerRound = safe_divide(kills, roundsPlayed)
    damagePerRound = safe_divide(damagePerRound, roundsPlayed)
    dDelta = safe_divide(dDelta, roundsPlayed)
    acs = safe_divide(acs, roundsPlayed)
    kast = safe_divide(kast, roundsPlayed)

    # Setup JSON
    json_data = {
                #'currentRank' : currentRank,
                #'gamesPlayed' : gamesPlayed,
                'name' : name,
                'winRate' : winRate,
                'hsPercent' : hsPercent,
                'Bodyshot Rate' : bsPercent,
                'Legshot Rate' : lsPercent,
                'kdRatio' : kda,
                #'kast' : kast, (For some reason round assist stat is broken so kast is currently broken)
                'dDelta' : dDelta,
                'acs' : acs,
                'kadRatio' : kadRatio,
                'killsPerRound' : killsPerRound,
                'roundWinPercent' : roundWinPercent,
                'damagePerRound' : damagePerRound,
            }
    
    return json_data

def average_data(file):
    with open(file, 'r') as infile:
        data = json.load(infile)

    players = data['players']
    totals = {}
    counts = {}

    for player in players:
        for field, value in player.items():
            try:
                totals[field] = totals.get(field, 0) + float(value)
                counts[field] = counts.get(field, 0) + 1
            except (ValueError, TypeError):
                continue

    averages = {
        field: round(totals[field] / counts[field], 2)
        for field in counts  # Use 'counts', not 'totals'
    }

    with open('averaged_stats.json', 'w') as outfile:
        json.dump(averages, outfile, indent=4)

# Credit stack overflow
def safe_divide(n, d):
    return n / d if d else 0