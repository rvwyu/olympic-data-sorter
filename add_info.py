import random
from datetime import datetime

def parse_date(date_str):
    '''
    attempts to parse a date string into a datetime object using multiple fallback strategies.
    
    the function assumes the input date_str may follow one or more of the formats below:
    
        1. "dd-mon-yyyy" (primary expected format, e.g. "17-jul-1990").
        2. "dd-mon-yy" where the two-digit year is converted to a four-digit year.
        3. "dd-month-yyyy" where the full month name is converted to its three-letter abbreviation.
        4. "dd-mon" where only day and abbreviated month are provided; defaults year to 1900.
        5. "dd month yyyy" (space-delimited), with conversion of the full month name if needed.
        6. a single 4-digit year (e.g. "1920"), which is interpreted as "01-jan-1920".
        7. "dd month" where the year is missing; defaults year to 1900.
        8. if the input is empty, it is treated as "01-jan-1900".
    
    parameters:
        date_str (str): the date string to be parsed.
    
    returns:
        datetime or none: returns a datetime object if parsing is successful; otherwise, returns none.
    '''
    if not date_str or date_str.strip() == "":
        # fallback for empty dates: default to "01-jan-1900"
        date_str = "01-Jan-1900"
    date_str = date_str.strip()

    # 1) primary attempt using expected cleaned format: "dd-mon-yyyy"
    try:
        return datetime.strptime(date_str, "%d-%b-%Y")
    except ValueError:
        pass

    # helper dictionary: full month name -> abbreviation
    month_map = {
        "January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr",
        "May": "May", "June": "Jun", "July": "Jul", "August": "Aug",
        "September": "Sep", "October": "Oct", "November": "Nov", "December": "Dec"
    }

    # 2) if dash-delimited, try to fix full month names or missing year
    if '-' in date_str:
        parts = [part.strip() for part in date_str.split('-')]
        if len(parts) == 2:
            # possibly "dd-mon" or "dd-month" format; default year to 1900
            day, month_part = parts
            if day.isdigit():
                if month_part in month_map:
                    month_part = month_map[month_part]
                guess = f"{day}-{month_part}-1900"
                try:
                    return datetime.strptime(guess, "%d-%b-%Y")
                except ValueError:
                    pass
        elif len(parts) == 3:
            # possibly "dd-mon-yy" or "dd-month-yyyy"
            day, month_part, year_part = parts
            # if month is a full month name, convert it
            if month_part in month_map:
                month_part = month_map[month_part]
            # if year is 2 digits, convert to four digits
            if len(year_part) == 2 and year_part.isdigit():
                yr = int(year_part)
                if 0 <= yr <= 10:
                    yr += 2000
                else:
                    yr += 1900
                year_part = str(yr)
            guess = f"{day}-{month_part}-{year_part}"
            try:
                return datetime.strptime(guess, "%d-%b-%Y")
            except ValueError:
                pass

    # 3) if space-delimited, try to use that format.
    tokens = date_str.split()
    if len(tokens) == 1:
        # possibly a single 4-digit year, interpreted as "01-jan-year"
        if tokens[0].isdigit() and len(tokens[0]) == 4:
            guess = f"01-Jan-{tokens[0]}"
            try:
                return datetime.strptime(guess, "%d-%b-%Y")
            except ValueError:
                pass
    elif len(tokens) == 2:
        # possibly "dd month" (e.g. "17 july"); default year to 1900
        day, month_token = tokens
        if day.isdigit():
            if month_token in month_map:
                month_token = month_map[month_token]
            guess = f"{day}-{month_token}-1900"
            try:
                return datetime.strptime(guess, "%d-%b-%Y")
            except ValueError:
                pass
    elif len(tokens) == 3:
        # possibly "dd month yyyy" (e.g. "17 july 1990")
        day, month_token, year_token = tokens
        if month_token in month_map:
            month_token = month_map[month_token]
        guess = f"{day}-{month_token}-{year_token}"
        try:
            return datetime.strptime(guess, "%d-%b-%Y")
        except ValueError:
            pass

    # 4) if all fallback methods fail, return none (debug message removed)
    # print(f"[debug] failed to parse date: '{date_str}'")
    return None

def compute_age(birth_date, event_date):
    '''
    computes the athlete's age at the time of the event.
    
    the calculation subtracts the birth year from the event year, and adjusts the age
    if the athlete's birthday has not been reached during that event year.
    
    parameters:
        birth_date (datetime): the athlete's birth date.
        event_date (datetime): the event (game) start date.
    
    returns:
        str: the age as a string if both dates are valid; returns an empty string otherwise.
    '''
    if not birth_date or not event_date:
        return ""
    age = event_date.year - birth_date.year
    if (event_date.month, event_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return str(age)

def add_age_full_date(event_results, birth_dates, game_dates):
    '''
    adds an "age" column to the event results data using the athlete's cleaned born date
    and the game start date.
    
    for each row in event_results, the function:
        - looks up the athlete's birth date (from birth_dates) and the game's start date (from game_dates)
        - parses both dates using parse_date() with fallback logic
        - computes the athlete's age using compute_age()
        - appends the computed age as a new column to the row
    
    parameters:
        event_results (list): two-dimensional list of event results. must include the headers 
                              "edition" and "athlete_id".
        birth_dates (dict):   dictionary mapping athlete_id to the cleaned born date string.
        game_dates (dict):    dictionary mapping edition to the game start date string.
    
    returns:
        list: the updated event_results list with an additional "age" column.
    '''
    # remove any bom from the header.
    if event_results[0][0].startswith('\ufeff'):
        event_results[0][0] = event_results[0][0].replace('\ufeff', '')
    header = event_results[0]
    if "edition" not in header or "athlete_id" not in header:
        print("error: required columns 'edition' or 'athlete_id' missing in event results.")
        return event_results
    idx_edition = header.index("edition")
    idx_athlete = header.index("athlete_id")
    header.append("age")
    
    for row in event_results[1:]:
        edition_str = row[idx_edition].strip()
        athlete_id = row[idx_athlete].strip()
        born_raw = birth_dates.get(athlete_id, "")
        game_raw = game_dates.get(edition_str, "")
        birth_dt = parse_date(born_raw)
        game_dt = parse_date(game_raw)
        row.append(compute_age(birth_dt, game_dt))
    
    return event_results

def build_birth_date_dict(athlete_bio):
    '''
    constructs a dictionary mapping each athlete's id to their cleaned birth date.
    
    assumes athlete_bio is a two-dimensional list with headers including "athlete_id" and "born".
    
    parameters:
        athlete_bio (list): two-dimensional list from 'olympic_athlete_bio.csv'.
    
    returns:
        dict: mapping where keys are athlete ids (str) and values are born date strings.
    '''
    birth_dates = {}
    if not athlete_bio:
        return birth_dates
    header = athlete_bio[0]
    try:
        idx_id = header.index("athlete_id")
        idx_born = header.index("born")
    except ValueError:
        print("athlete bio missing required columns ('athlete_id' or 'born').")
        return birth_dates
    for row in athlete_bio[1:]:
        if len(row) <= max(idx_id, idx_born):
            continue
        athlete_id = row[idx_id].strip()
        born_date = row[idx_born].strip()
        birth_dates[athlete_id] = born_date
    return birth_dates

def build_game_date_dict(games):
    '''
    constructs a dictionary mapping each olympic edition to its game start date.
    
    assumes games is a two-dimensional list with headers including "edition" and "start_date".
    
    parameters:
        games (list): two-dimensional list from 'olympics_games.csv'.
    
    returns:
        dict: mapping where keys are edition identifiers (str) and values are start date strings.
    '''
    game_dates = {}
    if not games:
        return game_dates
    header = games[0]
    try:
        idx_edition = header.index("edition")
        idx_start = header.index("start_date")
    except ValueError:
        print("games file missing required columns ('edition' or 'start_date').")
        return game_dates
    for row in games[1:]:
        if len(row) <= max(idx_edition, idx_start):
            continue
        edition_str = row[idx_edition].strip()
        start_date_str = row[idx_start].strip()
        game_dates[edition_str] = start_date_str
    return game_dates

def create_medal_tally(event_results, country_file):
    '''
    generates a medal tally summary from the event results data.
    
    the summary provides, for each country and olympic edition, the following:
        - edition, edition_id, country, country noc,
        - number of athletes,
        - number of gold, silver, and bronze medals,
        - total number of medals.
    
    parameters:
        event_results (list): two-dimensional list from 'olympic_athlete_event_results.csv'
                              with necessary columns.
        country_file (list): two-dimensional list from 'olympics_country.csv' with country data.
    
    returns:
        list: a two-dimensional list containing the medal tally summary with header:
              ["edition", "edition_id", "country", "country noc", "number_of_athletes",
               "number_of_gold", "number_of_silver", "number_of_bronze", "total_medals"].
    '''
    if not event_results:
        return []
    header = event_results[0]
    try:
        idx_edition = header.index("edition")
        idx_edition_id = header.index("edition_id")
        idx_country = header.index("country_noc")
        idx_athlete = header.index("athlete_id")
        idx_medal = header.index("medal")
    except ValueError:
        print("event results missing required columns.")
        return []
    
    # build a mapping from country noc to country name.
    country_map = {}
    if country_file:
        country_header = country_file[0]
        for row in country_file[1:]:
            if len(row) >= 2:
                noc = row[0].strip()
                country_name = row[1].strip()
                country_map[noc] = country_name
    
    tally = {}
    for row in event_results[1:]:
        edition_val = row[idx_edition].strip()
        country_noc = row[idx_country].strip()
        athlete_id = row[idx_athlete].strip()
        medal_txt = row[idx_medal].strip().lower()
        edition_id_val = row[idx_edition_id].strip() if idx_edition_id is not None else ""
        key = (edition_val, country_noc)
        if key not in tally:
            tally[key] = {
                "edition": edition_val,
                "edition_id": edition_id_val,
                "Country NOC": country_noc,
                "athlete_ids": set(),
                "gold": 0,
                "silver": 0,
                "bronze": 0
            }
        tally[key]["athlete_ids"].add(athlete_id)
        if medal_txt == "gold":
            tally[key]["gold"] += 1
        elif medal_txt == "silver":
            tally[key]["silver"] += 1
        elif medal_txt == "bronze":
            tally[key]["bronze"] += 1
    
    summary_header = [
        "edition", "edition_id", "country", "country noc", "number_of_athletes",
        "number_of_gold", "number_of_silver", "number_of_bronze", "total_medals"
    ]
    summary = [summary_header]
    for key in sorted(tally.keys()):
        data = tally[key]
        num_athletes = len(data["athlete_ids"])
        gold = data["gold"]
        silver = data["silver"]
        bronze = data["bronze"]
        total_medals = gold + silver + bronze
        country_name = country_map.get(data["Country NOC"], "")
        summary.append([
            data["edition"],
            data["edition_id"],
            country_name,
            data["Country NOC"],
            str(num_athletes),
            str(gold),
            str(silver),
            str(bronze),
            str(total_medals)
        ])
    return summary