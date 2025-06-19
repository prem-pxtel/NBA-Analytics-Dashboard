from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import alltimeleadersgrids



# Nikola Jokić
career = playercareerstats.PlayerCareerStats(player_id='203999') 

alltime = alltimeleadersgrids.AllTimeLeadersGrids()

# json
career.get_json()

# dictionary
# career.get_dict()
# print(career.get_dict())
# with open('career_stats.json', 'w') as f:
#     f.write(career.get_json())

print(alltime.get_json())
