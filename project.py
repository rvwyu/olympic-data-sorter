import files
from merge_paris_data import merge_paris
import clean_data
import add_info
import time 

start_time = time.perf_counter()

athlete_bio = files.read_csv_file("olympic_athlete_bio.csv")
athlete_event = files.read_csv_file("olympic_athlete_event_results.csv")
country = files.read_csv_file("olympics_country.csv")
games = files.read_csv_file("olympics_games.csv")
    
merge_paris(athlete_bio, athlete_event, country, games)
    
athlete_bio = files.read_csv_file("new_olympic_athlete_bio.csv")
athlete_event = files.read_csv_file("new_olympic_athlete_event_results.csv")
country = files.read_csv_file("new_olympics_country.csv")
games = files.read_csv_file("new_olympics_games.csv")
    
clean_data.cleanBornData(athlete_bio)
clean_data.cleanWeightData(athlete_bio)
clean_data.cleanHeightData(athlete_bio)
clean_data.cleanPosData(athlete_event)
clean_data.cleanMedalData(athlete_event)
clean_data.cleanDateGame(games)
clean_data.cleanIsHeld(games)
    
files.write_csv_file("new_olympic_athlete_bio.csv", athlete_bio)
files.write_csv_file("new_olympic_athlete_event_results.csv", athlete_event)
files.write_csv_file("new_olympics_country.csv", country)
files.write_csv_file("new_olympics_games.csv", games)
    
birth_dates = add_info.build_birth_date_dict(athlete_bio)
game_dates = add_info.build_game_date_dict(games)
    
updated_event = add_info.add_age_full_date(athlete_event, birth_dates, game_dates)
files.write_csv_file("new_olympic_athlete_event_results.csv", updated_event)

medal_tally = add_info.create_medal_tally(updated_event, country)
files.write_csv_file("new_medal_tally.csv", medal_tally)
    
print("Process completed successfully.")
    
end_time = time.perf_counter()
total_time = (end_time-start_time)
print(f"time for one()= {total_time}")