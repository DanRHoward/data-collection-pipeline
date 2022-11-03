class PL_Scrape:
    def __init__(self):
        import requests #package to retrieve html code of website
        from bs4 import BeautifulSoup

        html = requests.get("https://www.premierleague.com/stats/top/players/goals?se=489") #Gets the html code of the webpage
        html = html.content
        html = BeautifulSoup(html, 'html.parser') #Formats raw code into a more presentable way
        
        player_table = html.find_all('tr') #Returns all the table rows that we want
        list_player_stats = []
        for player in player_table[1:]:
            player_data = player.find_all('td') #gathers data from rows
            player_data = [feature.text for feature in player_data] #converts into a python list
            rank = player_data[0].replace('\n','')
            name = player_data[1].replace('\n','')
            nationality = player_data[3].replace('\n','')
            goals = player_data[4].replace('\n','')
            player_stats = {
                "Rank": rank,
                "Name": name,
                "Nationality": nationality,
                "Goals": goals
            }
            list_player_stats.append(player_stats)
        print(list_player_stats)

PL_Scrape()