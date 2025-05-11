import random

# Create prototypes for cleaning data in the Olympic files.
def cleanBornData(athletes):
    '''
    This function will clean the data in the 'born' column of the olympic_athlete_bio.csv file.
    It will be called after the Paris data is added into the existing Olympic data.
    It will convert all the formats of the date of birth to the format 'dd-Mon-yyyy'.
    It will handle the following cases:
        1. If the date is empty, the function will set it as an empty string.
        2. If the date is in the format 'dd-Mon-yy', the function will convert it to 'dd-Mon-yyyy'.
        3. If the date is in the format 'yyyy', the function will convert it to '01-Jan-yyyy'.
        4. If the date is in the format 'dd Month yyyy', the function will convert it to 'dd-Mon-yyyy'.
        5. If the date has only the year and month, the function will convert it to 'dd-Mon-yyyy', while 'dd' is a random number within the month.
        6. If the date has birthplace, the function will convert it to '01-Jan-1900'.
        7. If the date has year only, the function will convert it to '01-Jan-yyyy'.
        8. If the date has only the day and month, the function will convert it to 'dd-Mon-yyyy', while 'yyyy' is a random number between 1900 and 2000.
     
    Parameters:
        athletes (list): two-dimensional list of data from 'olympic_athlete_bio.csv'.
        
    Returns:
        No return.
    '''
    
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
             'December' : 'Dec'}
    
    born_column = -1
    headers = athletes[0]
    for i in range(0,len(athletes[0])):
        if headers[i] == 'born':
            born_column = i
        
    for row in athletes[1:]:
        born_date = row[born_column]
        
        # Case 1: empty
        if not born_date:
            row[born_column] = ""
            continue
        
        splitted_date = born_date.split('-')
        if len(splitted_date) == 3:
            
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
        
        
        elif len(splitted_date) == 2 and (splitted_date[0].isdigit() or splitted_date[1].isdigit()):
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
            splitted_date = born_date.split(' ')
            
            # Case 3: yyyy
            if len(splitted_date) == 1:
                day = '01'
                month = 'Jan'
                year = splitted_date[0]
                row[born_column] = f'{day}-{month}-{year}'
                
            elif len(splitted_date) == 2:
                
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
                
            elif len(splitted_date) == 3:
                
                # Case 4: dd Month yyyy
                if splitted_date[0].isdigit():
                    for month in months:
                        if splitted_date[1] == month:
                            splitted_date[1] = months[month]
                
                    if int(splitted_date[0]) < 10:
                        splitted_date[0] = f'0{splitted_date[0]}'
                    
                    row[born_column] = '-'.join(splitted_date)
                    
                       
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
                
def cleanWeightData(athletes):
    '''
    This function will clean the data in the 'weight' column of the olympic_athlete_bio.csv file.
    It will be called after the Paris data is added into the existing Olympic data.
    It will handle the following case:
        1. If the data is empty, the function will set it to 0.
        
    Parameters:
        athletes (list): two-dimensional list of data from 'olympic_athlete_bio.csv'.
        
    Returns:
        No return.
    '''
    weight_column = -1
    headers = athletes[0]
    
    for i in range(len(headers)):
        if headers[i] == 'weight':
            weight_column = i
    
    for row in athletes[1:]:
        if not row[weight_column]:
            row[weight_column] = 0

def cleanHeightData(athletes):
    '''
    This function will clean the data in the 'height' column of the olympic_athlete_bio.csv file.
    It will be called after the Paris data is added into the existing Olympic data.
    It will handle the following case:
        1. If the data is empty, the function will set it to 0.
        
    Parameters:
        athletes (list): two-dimensional list of data from 'olympic_athlete_bio.csv'.
        
    Returns:
        No return.
    '''
    height_column = -1
    headers = athletes[0]
    
    for i in range(len(headers)):
        if headers[i] == 'height':
            height_column = i
    
    for row in athletes[1:]:
        if not row[height_column]:
            row[height_column] = 0

def cleanPosData(eventResults):
    '''
    This function will clean the data in the 'pos' column of the olympic_athlete_event_results.csv file.
    It will be called after the Paris data is added into the existing Olympic data.
    It will handle the following cases:
        1. If the data of 'pos' column is empty, the function will set it as an empty string.
        2. If the data of 'pos' column starts with '=', the function will remove '='.
        
    Parameters:
        eventResults (list): two-dimensional list of data from 'olympic_athlete_event_results.csv'.
        
    Returns:
        No return.
    '''
    
    pos_column = -1
    headers = eventResults[0]
    
    for i in range(len(headers)):
        if headers[i] == 'pos':
            pos_column = i
    
    for row in eventResults[1:]:
        if not row[pos_column]:
            row[pos_column] = ''
        elif row[pos_column][0] == '=':
            row[pos_column] = row[pos_column][1:]

def cleanMedalData(eventResults):
    '''
    This function will clean the data in the 'medal' column of the olympic_athlete_event_results.csv file.
    It will be called after the Paris data is added into the existing Olympic data.
    It will handle the following cases:
        1. If the data of 'medal' column is empty, the function will set it as an empty string.
        2. The function will change the format of the data of 'medal' column to 'Gold', 'Silver', and 'Bronze' to be consistent.
        
    Parameters:
        eventResults (list): two-dimensional list of data from 'olympic_athlete_event_results.csv'.
        
    Returns:
        No return.
    '''
    
    medal_column = -1
    headers = eventResults[0]
    
    for i in range(len(headers)):
        if headers[i] == 'medal':
            medal_column = i
    
    for row in eventResults[1:]:
        if not row[medal_column]:
            row[medal_column] = ''
        elif len(row[medal_column].split(' ')) == 2:
            row[medal_column] = row[medal_column].split(' ')[0]

def cleanDateGame(games):
    '''
    This function will clean the data in the 'start_date' and 'end_date' columns of the olympics_games.csv file.
    It will be called after the Paris data is added into the existing Olympic data.
    It will handle the following case:
        1. If the data is empty, the function will set it as an empty string.
        
    Parameters:
        games (list): two-dimensional list of data from 'olympics_games.csv'.
        
    Returns:
        No return.
    '''
    
    start_date_column = -1
    end_date_column = -1
    headers = games[0]
    
    for i in range(len(headers)):
        if headers[i] == 'start_date':
            start_date_column = i
        elif headers[i] == 'end_date':
            end_date_column = i
    
    for row in games[1:]:
        if not row[start_date_column]:
            row[start_date_column] = '-'
        if not row[end_date_column]:
            row[end_date_column] = '-'

def cleanIsHeld(games):
    '''
    This function will clean the data in the 'isHeld' column of the olympics_games.csv file.
    It will be called after the Paris data is added into the existing Olympic data.
    It will handle the following case:
        1. If the data of 'isHeld' column is missing, the function will convert it to 'Held' or 'Not Held' by checking the "competition_date" column.
        
    Parameters:
        games (list): two-dimensional list of data from 'olympics_games.csv'.
        
    Returns:
        No return.
    '''
    
    isHeld_column = -1
    competition_date_column = -1
    headers = games[0]
    
    for i in range(len(headers)):
        if headers[i] == 'isHeld':
            isHeld_column = i
        elif headers[i] == 'competition_date':
            competition_date_column = i
    
    for row in games[1:]:
        if not row[isHeld_column]:
            if not row[competition_date_column] or len(row[competition_date_column]) == 1:
                row[isHeld_column] = 'Not held'
            else:
                row[isHeld_column] = 'Held'