from typing import Union

from dotenv import load_dotenv
import os
import time

import tbapy
import statbotics


load_dotenv()
statbot = statbotics.Statbotics()
tba = tbapy.TBA(os.getenv("TBA_API_KEY"))
year = 2025
db_path = 'Fim Graph 2025/'


class Event:
    def __init__(self, key: str, event_type: int, name: str, week: int, team_keys: list) -> None:
        self.key = key
        self.event_type = event_type
        self.name = name
        self.week = week
        self.team_keys = team_keys
        self.teams = []

    @classmethod
    def from_tba_event(cls, tba_event: dict) -> 'Event':
        tba_team_keys = tba.event_teams(tba_event.key, keys=True) # type: ignore
        if tba_event.week is None and (tba_event.event_type_string == 'Championship Division' or tba_event.event_type_string == 'Championship Finals'): # type: ignore
            week = 7
        else:
            week = int(tba_event.week) + 1 # type: ignore
        return cls(tba_event.key, tba_event.event_type, tba_event.name, week, tba_team_keys) # type: ignore

    @classmethod
    def from_md(cls, file_path: str) -> 'Event':
        with open(file_path, 'r') as file:
            lines = file.readlines()
            key = lines[1].split(':')[1].strip()
            event_type = int(lines[2].split(':')[1].strip())
            name = lines[3].split(':')[1].strip()
            week = int(lines[4].split(':')[1].strip())
            # team_keys = [line.strip().replace('[[', '').replace(']]', '') for line in lines[5:]]
            team_keys = []
            for line in lines[7:]:
                if line.__contains__('['):
                    team_keys.append(line.strip().replace('[[', '').replace(']]', ''))
            return cls(key, event_type, name, week, team_keys)

    def to_md(self, dir: str):
        os.makedirs(dir, exist_ok=True)
        with open(dir + str(self.key) + '.md', 'w') as file:
            print('saving event', self.key, 'to', file.name)
            text = '---\n'
            text += 'key: ' + str(self.key) + '\n'
            text += 'event_type: ' + str(self.event_type) + '\n'
            text += 'name: ' + str(self.name) + '\n'
            text += 'week: ' + str(self.week) + '\n'
            text += 'type: Event\n---\n'
            # text += 'teams: \n'
            # for team_key in self.team_keys:
            #     text += '- ' + str(team_key) + '\n'
            # text += '---\n'
            for team_key in self.team_keys:
                text += '[[' + str(team_key) + ']]\n'
            file.write(text)
 

class Team:
    def __init__(self, key: str, number: int, name: str, event_keys: list[str],
                 epa_end: float=0, 
                 auto_epa_end: float=0, 
                 teleop_epa_end: float=0, 
                 endgame_epa_end: float=0, 
                 winrate: float=0, 
                 district_epa_rank: int=0, 
                 district_epa_percentile: float=0) -> None:
        self.key                     = key
        self.number                  = number
        self.name                    = name
        self.event_keys              = event_keys
        self.epa_end                 = epa_end
        self.auto_epa_end            = auto_epa_end
        self.teleop_epa_end          = teleop_epa_end
        self.endgame_epa_end         = endgame_epa_end
        self.winrate                 = winrate
        self.district_epa_rank       = district_epa_rank
        self.district_epa_percentile = district_epa_percentile

    @classmethod
    def from_tba_team(cls, tba_team: dict):
        key = tba_team.key # type: ignore
        name = tba_team.nickname # type: ignore
        team_number = int(tba_team.team_number) # type: ignore

        try:
            statbot_stats = statbot.get_team_year(team_number, year, fields=[
                'epa_end', 'auto_epa_end', 'teleop_epa_end', 'endgame_epa_end', 'winrate', 'district_epa_rank', 'district_epa_percentile'
            ])
        except:
            statbot_stats = {}
        event_keys = tba.team_events(key, year, keys=True)
 
        return cls(key, team_number, name, event_keys, **statbot_stats)

    @classmethod
    def from_md(cls, file_name: str):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            key = lines[1].split(':')[1].strip()
            number = int(lines[2].split(':')[1].strip())
            name = lines[3].split(':')[1].strip()
            epa_end = float(lines[4].split(':')[1].strip())
            auto_epa_end = float(lines[5].split(':')[1].strip())
            teleop_epa_end = float(lines[6].split(':')[1].strip())
            endgame_epa_end = float(lines[7].split(':')[1].strip())
            winrate = float(lines[8].split(':')[1].strip())
            district_epa_rank = int(lines[9].split(':')[1].strip())
            district_epa_percentile = float(lines[10].split(':')[1].strip())
            event_keys = [line.strip().replace('[[', '').replace(']]', '') for line in lines[12:]]
            return Team(key, number, name, event_keys, epa_end, auto_epa_end, teleop_epa_end, endgame_epa_end, winrate, district_epa_rank, district_epa_percentile)

    def to_md(self, dir: str):
        os.makedirs(dir, exist_ok=True)
        with open(dir + str(self.key) + '.md', 'w', encoding='utf-8') as file:
            print('saving team', self.key, 'to', file.name)
            text = '---\n' 
            text += 'key: ' + str(self.key) + '\n'
            text += 'number: ' + str(self.number) + '\n'
            text += 'name: ' + str(self.name) + '\n'
            text += 'epa_end: ' + str(self.epa_end) + '\n'
            text += 'auto_epa_end: ' + str(self.auto_epa_end) + '\n'
            text += 'teleop_epa_end: ' + str(self.teleop_epa_end) + '\n'
            text += 'endgame_epa_end: ' + str(self.endgame_epa_end) + '\n'
            text += 'winrate: ' + str(self.winrate) + '\n'
            text += 'district_epa_rank: ' + str(self.district_epa_rank) + '\n'
            text += 'district_epa_percentile: ' + str(self.district_epa_percentile) + '\n'
            text += 'type: Team\n---\n'
            # text += 'events: \n'
            # for event_key in self.event_keys:
            #     text += '- ' + str(event_key) + '\n'
            # text += '---\n'
            for event_key in self.event_keys:
                text += '[[' + str(event_key) + ']]\n'
            file.write(text)


def load_events(event_keys: set[str]) -> list[Event]:
    def _query_event_from_tba(event_key: str) -> Union[None, Event]:
        print('querying tba for:', event_key)
        tba_event = tba.event(event_key, simple=False)
        
        try:
            if tba_event.event_type_string == 'Offseason' or tba_event.event_type_string == 'Preseason':
                return None

            event = Event.from_tba_event(tba_event)
            event.to_md(db_path + 'Events/')
            return event

        except:
            print('problem with event: ' + event_key)
            return None


    def _extract_event_from_file(file_name: str) -> Event:
        return Event.from_md(file_name)

    events = []

    for event_key in event_keys:
        file_name = db_path + 'Events/' + str(event_key) + '.md'
        # print(file_name)
        try:
            event = _extract_event_from_file(file_name)

        except Exception as e:
            # print(e)
            event = _query_event_from_tba(event_key)

        if event is not None:
            events.append(event)

    return events


def load_teams(team_keys: set[str]) -> list[Team]:
    '''loads the teams from a list of team keys. 
    If a local database exists, then the teams will be loaded form there.
    Otherwise, the teams will be loaded form api calls to TBA and statbotics, and the database created

    Parameters
    ----------
    team_keys : set[str]
        The set keys of the teams to load.
        Team keys take the form frc# -> frc####

    Returns
    -------
    list[Team]
        List of teams
    '''
    def _query_team_from_tba(team_key: str) -> Team:
        '''Internal function to load teams from the blue alliance

        Parameters
        ----------
        team_key : str
            The key of the teams to load.
            Team keys take the form frc# -> frc####

        Returns
        -------
        Team
            The loaded team
        '''
        print('querying tba for:', team_key)
        tba_team = tba.team(team_key, simple=False)
        team = Team.from_tba_team(tba_team)
        team.to_md(db_path + 'Teams/')
        return team

    def _extract_team_from_file(file_name: str) -> Team:
        '''Internal function to load teams from the database.

        Parameters
        ----------
        file_name : str
            The file name and path

        Returns
        -------
        Team
            The loaded team
        '''
        return Team.from_md(file_name)

    teams = []

    for team_key in team_keys:
        file_name = db_path + '/Teams/' + str(team_key) + '.md'
        try:
            team = _extract_team_from_file(file_name)

        except Exception as e:
            print(e)
            team = _query_team_from_tba(team_key)

        teams.append(team)

    return teams


def extract_team_keys_from_events(events: list[Event]) -> set[str]:
    team_keys = set()
    for event in events:
        for team_key in event.team_keys:
           team_keys.add(team_key)

    return team_keys


def main():
    teams = load_teams(set(tba.teams(year=2025, keys=True)))
    events = load_events(set(tba.events(year=2025, keys=True)))


if __name__ == '__main__':
    main()
