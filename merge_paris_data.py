import files

class Athletes:
    '''
    Used BST
    '''
    class Node:
        def __init__(self,data=None,left=None,right=None):
            self.data = data
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None

    def insert(self, data, isNew):
        if self.root is None:
            # we never insert new athlete data at root so this will not check 'isNew'
            self.root = Athletes.Node(data)
        else:
            curr = self.root
            inserted = False

            while not inserted:
                if data[0] < curr.data[0]:
                    if curr.left is not None:
                        curr = curr.left
                    else:
                        if isNew:
                            curr.left = Athletes.Node([data[0], data[2], data[5], data[17], 
                                                       data[13], data[14], data[8], data[7]])
                        else:
                            curr.left = Athletes.Node(data)
                        inserted = True
                else:
                    if curr.right is not None:
                        curr = curr.right
                    else:
                        if isNew:
                            curr.right = Athletes.Node([data[0], data[2], data[5], data[17], 
                                                       data[13], data[14], data[8], data[7]])
                        else:
                            curr.right = Athletes.Node(data)
                        inserted = True

    def search(self, id):
        curr = self.root

        while curr is not None:
            if id < curr.data[0]:
                curr = curr.left
            elif id > curr.data[0]:
                curr = curr.right
            else:
                return curr
        return None

    # These two functions are written to extract athlete data as list in ascending order for athlete_id
    def inorder_extract(self, result, subtree):
        if(subtree != None):
            self.inorder_extract(result, subtree.left)
            result.append(subtree.data)
            self.inorder_extract(result, subtree.right)
    def extract(self, full_athlete):
        self.inorder_extract(full_athlete, self.root)

class Athlete:
    '''
    To store data for details of merge_event_result
    '''
    def __init__(self, athlete, athlete_id, pos, medal):
        self.athlete = athlete
        self.athlete_id = athlete_id
        self.pos = pos
        self.medal = medal

    def get_data(self):
        return [self.athlete, self.athlete_id, self.pos, self.medal]

class Event:
    '''
    To store data for each event result
    '''
    def __init__(self, sport, event, result_id):
        self.sport = sport
        self.event_name = event
        self.result_id = result_id
        self.isTeamSport = False

        self.results = []

    def change_isTeamSport(self):
        self.isTeamSport = not self.isTeamSport

    def add_detail(self, detail : Athlete):
        self.results.append(detail)

    def load_full_info(self, paris_info)->list:
        '''
        This function returns 2D-list to add into new_merge_event_results as rows

        Parameters:
            paris_info(list) : contains [edition, edition_id, country_noc] for Paris 2024

        Returns:
            list : a 2D-list which contains elements as
                [edition,edition_id,country_noc,sport,event,result_id,athlete,athlete_id,pos,medal,isTeamSport]
        '''
        full_data = []
        #Adding [edition,edition_id,country_noc,sport,event,result_id]
        default_info = [paris_info[0], paris_info[1], paris_info[2]
                        , self.sport, self.event_name, self.result_id]
        
        for result in self.results:
            info = default_info.copy()
            #Adding [athlete,athlete_id,pos,medal]
            athlete = result.get_data()
            info.extend([athlete[0], athlete[1], athlete[2], athlete[3]])

            #Adding [isTeamSport]
            info.append(str(self.isTeamSport))
            full_data.append(info)
        return full_data

def merge_paris(athlete_data, event_data, country_data, game_data):
    '''
    This function merges existing Olympic data with Paris data.
    This reads the data in the Paris folder.
    It then calls each function that creates the newly needed file along with the required data.
        Call order of merge function:
            1. merge_games()
            2. merge_athlete()
            3. merge_country()
            4. merge_event_results()
    It will call read_csv_file() in files.py.

    Parameters:
        athlete_data(list): two-dimensional list of data from 'olympic_athlete_bio.csv'.
        event_data(list): two-dimensional list of data from 'olympic_athlete_event_results.csv'.
        country_data(list): two-dimensional list of data from 'olympics_country.csv'.
        game_data(list): two-dimensional list of data from 'olympics_games.csv'.

    Returns:
        No return.
    '''

    paris_athlete_data = files.read_csv_file("paris/athletes.csv")
    paris_event_data = files.read_csv_file("paris/events.csv")
    paris_medallists = files.read_csv_file("paris/medallists.csv")
    paris_country_data = files.read_csv_file("paris/nocs.csv")
    paris_team_data = files.read_csv_file("paris/teams.csv")

    paris_info = merge_games(game_data)
    merge_athlete(athlete_data, paris_athlete_data)
    merge_country(country_data, paris_country_data)
    merge_event_results(event_data, paris_info, paris_event_data, paris_medallists, paris_athlete_data, paris_team_data)

def merge_games(games) -> list:
    '''
    This function creates 'new_olympics_games.csv'.
    Then it will return a list which will be used
        when creating 'new_olympic_athlete_event_results.csv'.
    It will call write_csv_file() in files.py.

    Parameters:
        games(list): two-dimensional list of data from 'olympics_games.csv'.

    Returns:
        list: consists of ['edition', 'edition_id', 'country_noc'].
            This data is related to Paris 2024 Olympic.
    '''

    files.write_csv_file("new_olympics_games.csv", games)
    edition = []
    for game in games:
        if game[1] == "63":
            edition = [game[0], game[1], game[6]]
            break

    return edition

def merge_athlete(athlete_data, paris_athlete_data):
    '''
    This function creates 'new_olympic_athlete_bio.csv'.
    It merges original data with Paris data.
    It will add only new athlete data.
    It will call write_csv_file() in files.py.

    Parameters:
        athlete_data(list): two-dimensional list of data from 'olympic_athlete_bio.csv'.
        paris_athlete_data(list): two-dimensional list of data from athletes.csv.

    Returns:
        No return.
    '''
    athletes = Athletes()
    athletes_file_data = []

    # save original athlete data
    for idx in range(len(athlete_data) - 1):
        if idx == 0:
            athletes_file_data.append(athlete_data[idx])
        else:
            athletes.insert(athlete_data[idx], False)
    
    # save new athlete data
    for idx in range(len(paris_athlete_data) - 1):
        if idx != 0:
            if athletes.search(paris_athlete_data[idx][0]) == None:
                athletes.insert(paris_athlete_data[idx], True)

    # write merged data into new file
    athletes.extract(athletes_file_data)
    files.write_csv_file("new_olympic_athlete_bio.csv", athletes_file_data)

def merge_country(country_data, paris_country):
    '''
    This function creates 'new_olympics_country.csv'.
    It merges original data with Paris data.
    It will add only new country data.
    It will call write_csv_file() in files.py.

    Parameters:
        country_data(list): two-dimensional list of data from 'olympics_country.csv'.
        paris_country(list): two-dimensional list of data from nocs.csv.

    Returns:
        No return.
    '''

    for idx in range(len(paris_country) - 1):
        if idx != 0:
            if paris_country[idx][4] != 'P':
                country_data.append([paris_country[idx][0], paris_country[idx][1]])

    files.write_csv_file("new_olympics_country.csv", country_data)

def merge_event_results(event_data, edition, paris_event, paris_medallist, paris_athlete_data, paris_team):
    '''
    This function creates 'new_olympic_athlete_event_results.csv'.
    It merges original data with Paris data.

    Parameters:
        event_data(list): two-dimensional list of data from 'olympic_athlete_event_results.csv'.
        edition(list): list from merge_games(); ['edition', 'edition_id', 'country_noc']
        paris_event(list): two-dimensional list of data from 'events.csv'.
        paris_medallist(list): two-dimensional list of data from 'medallists.csv'.
        paris_athlete_data(list): two-dimensional list of data from 'athletes.csv'.
        paris_team(list): two-dimensional list of data from 'teams.csv'.

    Returns:
        No return.
    '''
    new_result_id = search_the_max(event_data, 5)

    # {event: sport}
    event_info = {event[0] : event[2] for event in paris_event}
    # {(event, code_athlete): (medal_code, medal_type)}
    medal_info = {(medal[14], medal[18]) : (medal[2], medal[1]) for medal in paris_medallist}
    # {(name, code): events}
    athlete_info = {(athlete[2], athlete[0]) : athlete[16] for athlete in paris_athlete_data}
    # [events]
    teams_event = [team[9] for team in paris_team]

    for event, sport in event_info.items():
        new_event = Event(sport, event, new_result_id)
        new_result_id+=1
        
        for (athlete_name, athlete_id), athlete_events in athlete_info.items():
            if event in athlete_events:
                for (medal_event, code_athlete), (medal_code, medal_type) in medal_info.items():
                    if event == medal_event and athlete_id == code_athlete:
                        detail = Athlete(athlete_name, athlete_id, medal_code, medal_type)
                        new_event.add_detail(detail)

        if event in teams_event:
            new_event.change_isTeamSport()

        event_data.extend(new_event.load_full_info(edition))    

    files.write_csv_file("new_olympic_athlete_event_results.csv", event_data)

def search_the_max(data_set, column)->int:
    '''
        This function finds a row which has biggest/largest value in the two-dimensional list 

        Parameters:
            data_set(list): the two-dimensional list
            column(int): the column of elements to be evaluated

        Returns:
            int: If found, the value of row. Otherwise, -1.
        '''
    max = -1
    for idx in range(1, len(data_set) - 1):
        key = int(data_set[idx][column].strip())
        if key > max:
            max = key
    return max