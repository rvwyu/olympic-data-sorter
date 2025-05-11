# Data analysis

## What unknown wrong data is there.

The dataset has multiple inconsistencies that impact accuracy and integration. These issues fall into four key categories: format inconsistencies, missing values, duplicate records, and structural mismatches.

1) Formatting Issues

athletes.csv → The "born" column is inconsistent, with some entries missing the month and day, some only listing the year, and others mistakenly including birthplaces.

medallists.csv → The "pos" column contains unnecessary "=" symbols that need to be removed for consistency.

events.csv → Event names do not always align with medallists.csv, which could cause mismatches when linking competition results.

2) Missing Information

athletes.csv → Several athletes have missing "height" and "weight" data.

medallists.csv → Some athletes have blank entries in the "medal" column, making it unclear if they placed or not.

olympics_games.csv → Missing values in "start_date," "end_date," and "isHeld" make it uncertain whether certain events actually took place.

teams.csv → Gaps exist in fields like "coaches," "num_athletes," "events," and "athletes_codes," which affects team-based analyses.

3) Duplicate Entries

nocs.csv → The dataset contains duplicate records for "ROC" (Russian Olympic Committee), which could lead to errors in country-based reporting and aggregation.

4) Structural Mismatches

events.csv vs. medallists.csv → Some event names are inconsistent across files, making it harder to correctly associate results and determine which athletes competed in specific events.

By addressing these issues, we can significantly improve the dataset’s reliability, ensuring accurate analysis and integration with the Paris data.

## How will wrong/unknown data be handled?

1. olympic_athlete_bio.csv file

   - In this file, there is an inconsistent format in the "born" column and some data is missing. Moreover, some data is incomplete and wrong, such as it just has year only, day and month only, month and year only, or birth place there.
   - If data is in an inconsistent format, I will split the strings into arrays and reformat them into the form which is "dd-Mon-yyyy".
   - If data is missing, I will make that data as empty strings.
   - If data is incomplete:

     - If data has year only, I will set the day and month to 01 and Jan respectively.
     - If data has day and month only, I will set the year based on a random number between 1900 and 2000.
     - If data has month and year only, I will identify the month to set a day randomly.
     - If data has birth place, I will set that data to a fixed date which is "01-Jan-1900".

   - There are two more columns with missing data that are "height" and "weight". I will handle this by setting missing data to 0 to represent that the data is missing.

2. olympic_athlete_event_results.csv

   - In this file, there is an inconsistent format in the "pos" column and some data is missing in the "medal" column.
   - In the "pos" column, some data starts with the "=" sign and I will handle it by removing the "=" sign at the beginning of the data.
   - In the "medal" column, some data is missing and I will make the missing data as empty strings to represent that there is no medal.

3. olympics_country.csv

   - In this file, there is one duplicated value which is "ROC" in the "noc" column and I will handle it by removing the duplicated one.

4. olympics_games.csv

   - In this file, there is missing data in the "start_date", "end_date", "isHeld" columns.
   - In the "start_date" and "end_date" columns, I will make the missing data as empty strings.
   - In the "isHeld" column, if the games were held by checking the "competition_date" column, I will make the missing data as "Held". Otherwise, I will make the missing data as "Not Held"

5. athletes.csv

   - In this file, there is missing data in the "birth_place", "birth_country", "residence_place", "residence_country" and I will handle it by making the missing data as empty strings.

6. medallists.csv

   - In this file, there is missing data in the "team", "team_gender", "url_event", "code_team" and I will handle it by making the missing data as empty strings in the "team", "url_event", "code_team" columns and empty characters in the "team_gender" column.

7. teams.csv

   - In this file, there is missing data in the "coaches", "coaches_codes", "num_coaches", "events", "athletes", "athletes_codes", "num_athletes" columns.
   - In the "athletes", "athletes_codes", "coaches", and "coaches_codes" columns, I will handle the missing data by setting the empty arrays.
   - In the "events" column, I will make the missing data as empty strings.
   - In the "num_athletes" and "num_coaches" columns, I will set the missing data to 0 to represent the missing data.

## How will Paris data be encorporated into data file?

1. _new_olympics_games_

   - There is no data to be encorporated in this file from Paris data.
   - Instead, the 'edition', 'edition_id', and 'country_noc' for Paris 2024 in this file will be used as the 'edition', 'edition_id', and 'country_noc' in the *new_olympic_athlete_event_results*.

2. _new_olympic_athlete_bio_
   | Olympic | Paris(_athletes.csv_) |
   | ------- | ----- |
   | athlete_id | code |
   | name | name |
   | sex | gender |
   | born | birth_date |
   | height | height |
   | weight | weight |
   | country | country |
   | country_noc | country_code |

   - Extract the required data from athletes.csv and create a dictionary. (It will follow the table above)
   - The key of that dictionary will be an athlete_id, and the value will be a list type containing other data.
   - Compare the key value of the newly created dictionary with the athlete_id in the existing *olympic_athlete_bio* and record it in a new file only if it does not exist.

3. _new_olympics_country_
   | Olympic | Paris(_nocs.csv_) |
   | ------- | ----- |
   | noc | code |
   | country | country |

   - We found that if the **'note'** value in the _nocs.csv_ file is not **'P'**, it is a country that is not recorded in the existing _olympics_country_.
   - Extract 'code', 'country', and 'note' from nocs.csv and make a list.
   - If the 'note' value is not 'P', write the data to the new file.

4. _new_olympic_athlete_event_results_
   | Olympic | _olympics_games.csv_ | _events.csv_ | _medallists.csv_ | _athletes_ | _teams.csv_ |
   | ------- | -------------------- | ------------ | --------------- | ---------- | ----------- |
   | edition | edition | | | | |
   | edition_id | edition_id | | | | |
   | country_noc | country_noc | | | | |
   | sport | | sport | | | |
   | event | | event | | | |
   | result_id | | event | | | |
   | athlete | | | | name | |
   | athlete_id | | | | code | |
   | pos | | | medal_code | | |
   | medal | | | medal_type | | |
   | isTeamSport | | | | | events |

   - Sort the original record into a new file based on the ‘result_id’.
   - Then save the largest ‘result_id’.
   - Create a class named ‘Event’.
     - It will have ‘my_event’ (event).
     - It will have 'event_details' as list type which will be the list of [sport, result_id, athlete, athlete_id, pos, medal, isTeamSport] in order.
   - Repeat the steps below for all ‘event’ in *events.csv*.
     - First, create an instance of ‘Event’ and initialize ‘my_events’ as 'event'.
     - Compare the ‘sport’ of events.csv with the element of ‘disciplines’ in *athletes.csv*.
     - If the same value is found, check if the athletes has same element in ‘events’ as the ‘event’ in *events.csv*.
     - If this value is also matched, add the relevant value to the value of ‘my_events’. (values will be added: [sport, result_id, athlete, athlete_id, None, None, False]).
     - Here, ‘result_id’ is the previously stored value and will be stored with increment by 1 for a new event.
     - Above 6 steps will be iterated while it compares all *events.csv* records with *athletes.csv*.
   - Compare all the keys of ‘my_events’ stored here with the elements of ‘events’ in *teams.csv*.
     - Change the value of ‘isTeamSport’ in the 'event_details' to “True” if it finds same element.
   - Compare all of the ‘athlete_id’ in the 'event_details' with the ‘code_athlete’ in *medallists.csv*.
     - ‘medal_code’ in *medallist.csv* will be stored in ‘pos’ as an integer value if it is same.
     - ‘medal_type’ in *medallist.csv* will be stored in ‘medal’.
   - Add data in all instance of ‘Event’ into new file.
   - As we mentioned above, every 'edition', 'edition_id', and 'country_noc' will be same for all records to be added this time.

>  Required additional work:
>    > Currently, if the athlete is not a medalist, the 'pos' value is kept as None, unlike the existing record. We must decide whether we want to hard code this value or write down the code to retrieve it from the ‘sport_url’ in the *events.csv*.   
>    > The 'medal’ value stored now is different from the type of the existing record. (Example - Original: "Gold", New: "Gold medal").
