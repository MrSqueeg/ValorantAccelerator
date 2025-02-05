import get

def get_match_data(data, name):
    kills = 0
    deaths = 0
    kda = 0

    for match in data:
        players = match['players']['all_players']
        for player in players:
            if player['name'].lower() == name.lower():
                print(player['stats']['kills'])
                kills += player['stats']['kills']
                deaths += player['stats']['deaths']
                kda = kills / deaths

    get.save_data(f"kills: {kills}\ndeaths: {deaths}\nKDA: {kda}", "data.txt")