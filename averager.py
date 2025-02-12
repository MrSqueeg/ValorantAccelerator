import get
import json

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
                dDelta += player['stats']['damage']['dealt']
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
    roundWinPercent = roundsWon / roundsLost or 1
    winRate = winRate / matches
    roundsPlayed = roundsWon + roundsLost
    totalShots = ls+bs+hs
    hsPercent = hs / totalShots or 1
    bsPercent = bs / totalShots or 1
    lsPercent = ls / totalShots or 1
    kda = kills / deaths or kills
    kadRatio = (kills + assists) / deaths
    killsPerRound = kills / roundsPlayed
    damagePerRound = damagePerRound / roundsPlayed
    dDelta = dDelta / roundsPlayed
    acs = acs / roundsPlayed
    kast = kast / roundsPlayed

    # Setup JSON
    json_data = {
                #'currentRank' : currentRank,
                #'gamesPlayed' : gamesPlayed,
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

    outfile = open('stats.json', 'w')
    json.dump(json_data, outfile)   