# Analysis

## Describe the assumptions and decisions.

**Sang Yu Lee:**

- I decided to create a function 'merge_paris()' which controls all the merge functions, in order to use only this function from another file (project.py).
- While studying the _nocs.csv_ and _olympic_country.csv_, I found that when the 'note' is not 'P', the corresponding country does not exist in original olympic_country file.
- I found that there's no need to insert new data into _new_olympics_games.csv_, but I needed to extract data from it to insert new rows into _new_olympic_athlete_event_results.csv_.
- The decisions for data structures are written below.

**Hoang Phuc Huynh:**

- Cleaning data process begins after merging Paris data process finishes to ensure the data to be consistent.
- I decided to handle missing data by setting as empty strings. For example, when I cleaned born data in the olympic_athlete_bio file, if the data is missing, I just set it as an empty string.

**Rhowen Vaughn Wendelle Yu:**

- I used a helper function parse_date() to handle all kinds of birthdate formats, defaulting to "01-Jan-1900" if the input is empty.  
- For the "age" column, I created add_age_full_date() which computes age by comparing the athlete's parsed birth date and the start date of the games.  
- Missing or invalid dates return None and result in an empty string for the age.  
- I generated new_medal_tally.csv with create_medal_tally(), grouping by country and edition, counting medals, and tallying the total.  

## Describe the data structures you used in your application and whether you wrote your own or used a built in python data structure (anything beyond python list should be described)

> Describe the general way the data is manipulated by your program  
> If you have a dictionary, what is the key?  
> How fast is it to find the information that you need?  
> etc.

**Sang Yu Lee:**

1. **Athletes (class)**  
   This is an Binary Search Tree.  
   Each athlete's data is stored as a list in the node.  
   The time complexity of search() in this class will be O(log n) in average case or O(n) in worst case.
2. **Athlete (class)**  
   An instance of this class will contain [athlete, athlete_id, pos, medal].  
   This does not provide any time benefit for finding information.  
   This type will be used in Event class as 'results = [Athlete]'.
3. **Event (class)**  
   An instance of this class will contain sport, event_name, result_id, isTeamSport, [Athlete].  
   The 'load_full_info()' helps to create multiple rows that have same[ sport, event_name, result_id, isTeamSport] and differ in [athlete, athlete_id, pos, medal].
4. **edition (list) in merge_games()**  
   As I used 2D-list for file data, this list can be used as part of new data in event result data.  
   There's no need to search for information in this list. It can be used as is.
5. **event_info (dictionary) in merge_event_results()**  
   This dictionary is used for all events in paris data  
   {event: sport}  
   to map each event to its sport  
   I used this to extract only required data from full event data.
6. **medal_info (dictionary) in merge_evnet_results()**  
   This dictionary is used for all medal data in paris data  
   {(event, code_athlete): (medal_code, medal_type)}  
   to map medal information using the event name and the athlete code to the medal code and type.  
   I used this to extract only necessary data from full medal data.
7. **athlete_info (dictionary) in merge_event_results()**  
   This dictionary is used for all athlete data in paris data.  
   {(name, code): events}  
   to map each athlete information with name, code, and events(list).  
   I used this to get only necessary data from full athlete data.

**Hoang Phuc Huynh:**

- When I cleaned the born data, I used the dictionary to manage the months. In this dictionary, the key is the non-abbreviated names of 12 months in a year and the value is the shorthand forms of 12 months. I used this dictionary to replace the non-abbreviated month names with the shorthand month names in the records.

**Rhowen Vaughn Wendelle Yu:**

- For adding informations, birth_dates and game_dates are dictionaries that let me quickly (O(1)) look up birth and event dates for age calculation. month_map helped standardize inconsistent date formats. For the medal tally, I used a tally dictionary with (edition, country_noc) as the key to track medals and unique athletes. country_map linked NOC codes to full country names. Lists were used to hold the raw and processed data like spreadsheets.

## Analyze the following:

1.  runtime to clean all data
2.  runtime needed to add paris data into records
3.  runtime needed to generate the medal results for all games

> Use the following data size:
>
> > let n represent the number of records in the olympic_athlete_events_results file  
> > let a represent the number of records in the olympic_athlete_bio file  
> > let p represent the number of records in the paris athletes file  
> > let e represent the number of records in the paris events file  
> > let m represent the number of records in the paris medallists file.

1.  runtime to clean all data

- Cleaning born data

  - Let a represents the number of records in the olympic_athlete_bio file.

  - Let T(a) represents the number of operations necessary to perform cleaning data.

  ```python
  def cleanBornData(athletes):
  months = {'January' : 'Jan',
           'February' : 'Feb',
           'March':'Mar',
           'April': 'Apr',
           'May' : 'May',
           'June' : 'Jun',
           'July' : 'Jul',
           'August' : 'Aug',
           'September' : 'Sep',
           'October' : 'Oct',
           'November' : 'Nov',
           'December' : 'Dec'} # 1

  born_column = -1 # 1
  headers = athletes[0] # 1
  for i in range(0,len(athletes[0])): # 10
      if headers[i] == 'born': # 8
          born_column = i # 1

  for row in athletes[1:]: # a-1
      born_date = row[born_column] # a-1

      # Case 1: empty
      if not born_date: # a-1
          row[born_column] = ""
          continue

      splitted_date = born_date.split('-') # 2(a-1)
      if len(splitted_date) == 3: # 2(a-1)

          # Case 2: dd-Mon-yy
          if len(splitted_date[2]) == 2 and splitted_date[2].isdigit():
              year = int(splitted_date[2])
              if year >= 0 and year <= 10:
                  year = 2000 + year
              elif year >= 11 and year <= 99:
                  year = 1900 + year
              splitted_date[2] = str(year)
              row[born_column] = '-'.join(splitted_date)


          # Case 6: birthplace only
          else:
              day = '01'
              month = 'Jan'
              year = '1900'
              row[born_column] = f'{day}-{month}-{year}'


      elif len(splitted_date) == 2 and (splitted_date[0].isdigit() or splitted_date[1].isdigit()): # 6(a-1)
          # Case 8: day month only
          if splitted_date[0].isdigit():
              day = splitted_date[0]
              month = splitted_date[1]
              year = random.randint(1900,2000)
              row[born_column] = f'{day}-{month}-{year}'

          # Case 5: Mon-yyyy
          else:
              if splitted_date[1].isdigit():
                  day = 1
                  if splitted_date[0] == 'Feb':
                      day = 28
                  elif splitted_date[0] == 'Apr' or splitted_date[0] == 'Jun' or splitted_date[0] == 'Sep' or splitted_date[0] == 'Nov':
                      day = 30
                  else:
                      day = 31

                  day = random.randint(1, day)
                  if day < 10:
                      day = f'0{day}'
                  row[born_column] = f'{day}-{splitted_date[0]}-{splitted_date[1]}'

      else:
          splitted_date = born_date.split(' ') # 2(a-1)

          # Case 3: yyyy
          if len(splitted_date) == 1: # 2(a-1)
              day = '01'
              month = 'Jan'
              year = splitted_date[0]
              row[born_column] = f'{day}-{month}-{year}'

          elif len(splitted_date) == 2: #2(a-1)

              # Case 5: Month yyyy
              if splitted_date[1].isdigit():
                  for month in months:
                      if splitted_date[0] == month:
                          splitted_date[0] = months[month]
                  day = 1
                  if splitted_date[0] == 'Feb':
                      day = 28
                  elif splitted_date[0] == 'Apr' or splitted_date[0] == 'Jun' or splitted_date[0] == 'Sep' or splitted_date[0] == 'Nov':
                      day = 30
                  else:
                      day = 31

                  day = random.randint(1, day)
                  if day < 10:
                      day = f'0{day}'
                  row[born_column] = f'{day}-{splitted_date[0]}-{splitted_date[1]}'

              # Case 7: year only in format (c. yyyy) or (circa yyyy)
              else:
                  indexOfParenthesis = splitted_date[1].find(')')
                  day = '01'
                  month = 'Jan'
                  year = splitted_date[1][0:indexOfParenthesis]
                  row[born_column] = f'{day}-{month}-{year}'

          elif len(splitted_date) == 3: # 2(a-1)

              # Case 4: dd Month yyyy
              if splitted_date[0].isdigit(): # a-1
                  for month in months: # 12(a-1)
                      if splitted_date[1] == month: # 12(a-1)
                          splitted_date[1] = months[month] # (a-1)

                  if int(splitted_date[0]) < 10: # 2(a-1)
                      splitted_date[0] = f'0{splitted_date[0]}' # (a-1)

                  row[born_column] = '-'.join(splitted_date) # 2(a-1)


              else:
                  day = '01'
                  month = 'Jan'

                  # Case 7: year only in format (yyyy or yyyy)
                  if splitted_date[0][1:].isdigit():
                      year = splitted_date[0][1:]
                      row[born_column] = f'{day}-{month}-{year}'

                  #Case 6: birthplace only
                  else:
                      year = '1900'
                      row[born_column] = f'{day}-{month}-{year}'
          else:
              all_birthplace = True

              # Case 6: birthplace and year at the end
              for word in splitted_date:
                  indexOfParenthesis = word.find(')')
                  if indexOfParenthesis != -1 and word[:indexOfParenthesis].isdigit():
                      day = '01'
                      month = 'Jan'
                      year = word[:indexOfParenthesis]
                      row[born_column] = f'{day}-{month}-{year}'
                      all_birthplace = False
                      break

              # Case 6: birthplace only
              if all_birthplace:
                  day = '01'
                  month = 'Jan'
                  year = '1900'
                  row[born_column] = f'{day}-{month}-{year}'
  ```

  $$T(a) = 1 + 1 + 1 + 10 + 8 + 1 + (a-1) + (a-1) + (a-1) + 2(a-1) + 2(a-1) + 6(a-1) + 2(a-1) + 2(a-1) + 2(a-1) + 2(a-1) + (a-1) + 12(a-1) + 12(a-1) + (a-1) + 2(a-1) + (a-1) + 2(a-1)$$  
  $$T(a) = 22 + 52(a-1) = 22 + 52a - 52 = 52a - 30$$  
  Therefore, $T(a)$ is $O(a)$ if and only if $c = 53$ and $a_{0} = 1$

- Cleaning weight data

  - Let a represents the number of records in the olympic_athlete_bio file.

  - Let T(a) represents the number of operations necessary to perform cleaning data.

  ```python
  def cleanWeightData(athletes):
  weight_column = -1 # 1
  headers = athletes[0] # 1

  for i in range(len(headers)): # 10
      if headers[i] == 'weight': # 8
          weight_column = i # 1

  for row in athletes[1:]: # a-1
      if not row[weight_column]: # a-1
          row[weight_column] = 0 # a-1
  ```

  $$T(a) = 1 + 1 + 10 + 8 + 1 + (a-1) + (a-1) + (a-1)$$  
  $$T(a) = 21 + 3(a-1) = 3a + 18$$  
  Therefore, $T(a)$ is $O(a)$ if and only if $c=12$ and $a_{0}=2$

- Cleaning height data

  - Let a represents the number of records in the olympic_athlete_bio file.

  - Let T(a) represents the number of operations necessary to perform cleaning data.

  ```python
  def cleanHeightData(athletes):
    height_column = -1 # 1
    headers = athletes[0] # 1

    for i in range(len(headers)): # 10
        if headers[i] == 'height': # 8
            height_column = i # 1

    for row in athletes[1:]: # a-1
        if not row[height_column]: # a-1
            row[height_column] = 0 # a-1
  ```

  $$T(a) = 1 + 1 + 10 + 8 + 1 + (a-1) + (a-1) + (a-1)$$  
  $$T(a) = 21 + 3(a-1) = 3a + 18$$  
  Therefore, $T(a)$ is $O(a)$ if and only if $c=12$ and $a_{0}=2$

- Cleaning Pos data

  - Let n represents the number of records in the olympic_athlete_events_results file.

  - Let T(n) represents the number of operations necessary to perform cleaning data.

  ```python
  def cleanPosData(eventResults):
    pos_column = -1 # 1
    headers = eventResults[0] # 1

    for i in range(len(headers)): # 10
        if headers[i] == 'pos': # 8
            pos_column = i # 1

    for row in eventResults[1:]: # n-1
        if not row[pos_column]: # n-1
            row[pos_column] = ''
        elif row[pos_column][0] == '=': # n-1
            row[pos_column] = row[pos_column][1:] # n-1
  ```

  $$T(n) = 1 + 1 + 10 + 8 + 1 + (n-1) + (n-1) + (n-1) + (n-1)$$  
  $$T(n) = 21 + 4(n-1) = 4n + 17$$  
  Therefore, $T(n)$ is $O(n)$ if and only if $c=12$ and $n_{0}=3$

- Cleaning medal data

  - Let n represents the number of records in the olympic_athlete_events_results file.

  - Let T(n) represents the number of operations necessary to perform cleaning data.

  ```python
  def cleanMedalData(eventResults):
    medal_column = -1 # 1
    headers = eventResults[0] # 1

    for i in range(len(headers)): # 10
        if headers[i] == 'medal': # 8
            medal_column = i # 1

    for row in eventResults[1:]: # n-1
        if not row[medal_column]: # n-1
            row[medal_column] = ''
        elif len(row[medal_column].split(' ')) == 2: # 3(n-1)
            row[medal_column] = row[medal_column].split(' ')[0] #2(n-1)
  ```

  $$T(n) = 1 + 1 + 10 + 8 + 1 + (n-1) + (n-1) + 3(n-1) + 2(n-1)$$  
  $$T(n) = 21 + 7(n-1) = 7n + 14$$  
  Therefore, $T(n)$ is $O(n)$ if and only if $c=12$ and $n_{0}=3$

- Cleaning date game data

  - Let g represents the number of records in the olympics_games file.

  - Let T(g) represents the number of operations necessary to perform cleaning data.

  ```python
  def cleanDateGame(games):
    start_date_column = -1 # 1
    end_date_column = -1 # 1
    headers = games[0] # 1

    for i in range(len(headers)): # 10
        if headers[i] == 'start_date': # 8
            start_date_column = i
        elif headers[i] == 'end_date': # 8
            end_date_column = i # 1

    for row in games[1:]: # g-1
        if not row[start_date_column]: # g-1
            row[start_date_column] = '-' # g-1
        if not row[end_date_column]: # g-1
            row[end_date_column] = '-' # g-1
  ```

  $$T(g) = 1 + 1 + 1 + 10 + 8 + 8 + 1 + (g-1) + (g-1) + (g-1) + (g-1) + (g-1)$$  
  $$T(g) = 30 + 5(g-1) = 5g + 25$$  
  Therefore, $T(g)$ is $O(g)$ if and only if $c=18$ and $g_{0}=2$

- Cleaning isHeld data

  - Let g represents the number of records in the olympics_games file.

  - Let T(g) represents the number of operations necessary to perform cleaning data.

  ```python
  def cleanIsHeld(games):
    isHeld_column = -1 # 1
    competition_date_column = -1 # 1
    headers = games[0] # 1

    for i in range(len(headers)): # 10
        if headers[i] == 'isHeld': # 8
            isHeld_column = i
        elif headers[i] == 'competition_date': # 8
            competition_date_column = i # 1

    for row in games[1:]: # g-1
        if not row[isHeld_column]: # g-1
            if not row[competition_date_column] or len(row[competition_date_column]) == 1: # 4(g-1)
                row[isHeld_column] = 'Not held' # g-1
            else:
                row[isHeld_column] = 'Held'
  ```

  $$T(g) = 1 + 1 + 1 + 10 + 8 + 8 + 1 + (g-1) + (g-1) + 4(g-1) + (g-1)$$  
  $$T(g) = 30 + 7(g-1) = 7g + 23$$  
  Therefore, $T(g)$ is $O(g)$ if and only if $c=18$ and $g_{0}=3$

2.  runtime needed to add paris data into records

> > let n represent the number of records in the olympic_athlete_events_results file  
> > let p represent the number of records in the paris athletes file  
> > let e represent the number of records in the paris events file  
> > let m represent the number of records in the paris medallists file.
> > let t represent the number of records in the paris teams file.

```python
def merge_event_results(event_data, edition, paris_event, paris_medallist, paris_athlete_data, paris_team):
    new_result_id = search_the_max(event_data, 5) # n

    event_info = {event[0] : event[2] for event in paris_event} # e+1
    medal_info = {(medal[14], medal[18]) : (medal[2], medal[1]) for medal in paris_medallist} # m+1
    athlete_info = {(athlete[2], athlete[0]) : athlete[16] for athlete in paris_athlete_data} # p+1
    teams_event = [team[9] for team in paris_team] # t+1

    for event, sport in event_info.items(): # e
        new_event = Event(sport, event, new_result_id)  # e
        new_result_id+=1 #2e

        for (athlete_name, athlete_id), athlete_events in athlete_info.items(): # e*p
            if event in athlete_events: # e*p
                for (medal_event, code_athlete), (medal_code, medal_type) in medal_info.items(): # e*p*m
                    if event == medal_event and athlete_id == code_athlete: # 3(e*p*m)
                        detail = Athlete(athlete_name, athlete_id, medal_code, medal_type) # e*p*m
                        new_event.add_detail(detail) # e*p*m

        if event in teams_event: # e*t
            new_event.change_isTeamSport() # e*t

        event_data.extend(new_event.load_full_info(edition)) # e*p

    files.write_csv_file("new_olympic_athlete_event_results.csv", event_data) # n+e*p

def search_the_max(data_set, column)->int:
    max = -1 # 1
    for idx in range(1, len(data_set) - 1): # (n-1)
        key = int(data_set[idx][column].strip()) # (n-1)
        if key > max: # (n-1)
            max = key # (n-1)
    return max # 1

class Event:
    ...
    def change_isTeamSport(self):
        self.isTeamSport = not self.isTeamSport # 2

    def add_detail(self, detail : Athlete):
        self.results.append(detail) # 1

    def load_full_info(self, paris_info)->list:
        full_data = [] # 1
        default_info = [paris_info[0], paris_info[1], paris_info[2]
                        , self.sport, self.event_name, self.result_id] # 1

        for result in self.results: # p
            info = default_info.copy() # 2p
            athlete = result.get_data() # 2p
            info.extend([athlete[0], athlete[1], athlete[2], athlete[3]]) # p

            info.append(str(self.isTeamSport)) # p
            full_data.append(info) # p
        return full_data # 1

def write_csv_file(file_name, data_set):
    with open(file_name, mode='w', newline='', encoding="utf-8") as file: # 1
        csv_writer = csv.writer(file) # 2
        for row in data_set: # n+e
            csv_writer.writerow(row) # n+e
```

- search_the_max -> $$O(n)$$
- change_isTeamSport -> $$O(1)$$
- add_detail() -> $$O(1)$$
- load_full_info() -> $$O(1)$$
- write_csv_file() -> $$O(n+e)$$

**merge_event_results()** ->
$= 2n + 5e + m + p + t + 4ep + 6epm + 2et + 4$  
If only I left the dominant one...  
$T(n,p,e,m,t)$ is $O(epm)$

3. runtime needed to generate the medal results for all games

> > let n represent the number of records in the olympic_athlete_events_results file  
> > let p represent the number of records in the paris athletes file  
> > let e represent the number of records in the paris events file  
> > let m represent the number of records in the paris medallists file.
> > let t represent the number of records in the paris teams file.

```python
def create_medal_tally(event_results, country_file):
    if not event_results:                     # 1
        return []                           # 1

    header = event_results[0]                 # 1
    try:
        idx_edition = header.index("edition")         # 1
        idx_edition_id = header.index("edition_id")     # 1
        idx_country = header.index("country_noc")       # 1
        idx_athlete = header.index("athlete_id")          # 1
        idx_medal = header.index("medal")               # 1
    except ValueError:
        print("event results missing required columns.")  # 1
        return []                           # 1

    country_map = {}                          # 1
    if country_file:                          # 1
        country_header = country_file[0]      # 1
        for row in country_file[1:]:          # (k–1 iterations; ~4 ops each)
            if len(row) >= 2:                 # 1
                noc = row[0].strip()          # 1
                country_name = row[1].strip() # 1
                country_map[noc] = country_name  # 1

    tally = {}                                # 1
    for row in event_results[1:]:             # (n–1 iterations; ~18 ops each)
        edition_val = row[idx_edition].strip()       # 1
        country_noc = row[idx_country].strip()         # 1
        athlete_id = row[idx_athlete].strip()          # 1
        medal_txt = row[idx_medal].strip().lower()     # 2
        edition_id_val = row[idx_edition_id].strip()    # 1
        key = (edition_val, country_noc)               # 1
        if key not in tally:                           # 1
            tally[key] = {                             # 7
                "edition": edition_val,
                "edition_id": edition_id_val,
                "Country NOC": country_noc,
                "athlete_ids": set(),
                "gold": 0,
                "silver": 0,
                "bronze": 0
            }
        tally[key]["athlete_ids"].add(athlete_id)        # 1
        if medal_txt == "gold":                         # 1
            tally[key]["gold"] += 1                     # 1
        elif medal_txt == "silver":                     # 1
            tally[key]["silver"] += 1                   # 1
        elif medal_txt == "bronze":                     # 1
            tally[key]["bronze"] += 1                   # 1

    summary_header = [                           # 1
        "edition", "edition_id", "country", "country noc",
        "number_of_athletes", "number_of_gold",
        "number_of_silver", "number_of_bronze", "total_medals"
    ]
    summary = [summary_header]                    # 1

    for key in sorted(tally.keys()):            # O((n–1) log(n–1)) comparisons, then (n–1 iterations; ~18 ops each)
        data = tally[key]                       # 1
        num_athletes = len(data["athlete_ids"])   # 1
        gold = data["gold"]                       # 1
        silver = data["silver"]                   # 1
        bronze = data["bronze"]                   # 1
        total_medals = gold + silver + bronze     # 2
        country_name = country_map.get(data["Country NOC"], "")  # 1
        summary.append([                         # ~10
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

    return summary                             # 1

```
create_medal_tally -> O(1) + O(a) + O(n) + O(n log n) + O(1)
then, T(n, a) = O(n log n)
