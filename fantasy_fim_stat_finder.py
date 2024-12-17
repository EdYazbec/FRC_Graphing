from typing import Union

from dotenv import load_dotenv
import os
import time
import pandas as pd

import tbapy
import statbotics


load_dotenv()
statbot = statbotics.Statbotics()
tba = tbapy.TBA(os.getenv("TBA_API_KEY"))
year = 2025
db_path = 'Fim Graph 2025/'


def main():
    headers = ['key', 'number', 'name', 'Event_1_Week', 'Event_1_Key', 'Event_1_fused', 'Event_2_Week', 'Event_2_Key', 'Event_2_fused', 'EPA', 'Win_Rate', 'EPA_Rank', 'EPA_Percentile']
    table = []

    for tba_team in tba.district_teams("2025fim", simple=True):
        print('loading info for ' + tba_team['key'])
        try:
            statbot_team = statbot.get_team_year(int(tba_team['key'][3:]), year-1, fields=['winrate', 'district_epa_rank', 'district_epa_percentile', 'epa_end'])
            # for key in statbot.get_team_year(int(tba_team['key'][3:]), year-1).keys():
            #     print(key)
        except:
            statbot_team = {'winrate': 0, 'district_epa_rank': 0, 'epa_end': 0, 'district_epa_percentile': 0}
        row = []
        row.append(tba_team['key'])
        row.append(int(tba_team['key'][3:]))
        row.append(tba_team.get('nickname', 'Unknown'))  # Handle missing 'nickname'
        
        tba_events = tba.team_events(tba_team['key'], year)

        if len(tba_events) > 0:
            # Add details for the first event
            row.append(tba_events[0].get('week', None))
            row.append(tba_events[0].get('event_code', None))
            row.append(str(tba_events[0].get('week', None)) + tba_events[0].get('event_code', None))
        else:
            row.extend([None, None, None])  # Fill with None if no event data

        if len(tba_events) > 1:
            # Add details for the second event
            row.append(tba_events[1].get('week', None))
            row.append(tba_events[1].get('event_code', None))
            row.append(str(tba_events[1].get('week', None)) + tba_events[1].get('event_code', None))
        else:
            row.extend([None, None, None])  # Fill with None if only one event or none

        row.append(statbot_team['epa_end'])
        row.append(statbot_team['winrate'])
        row.append(statbot_team['district_epa_rank'])
        row.append(statbot_team['district_epa_percentile'])
        table.append(row)

    # Convert table to DataFrame
    df = pd.DataFrame(table, columns=headers)
    df.to_csv('fantasy_fim_worksheet_2025.csv')
    print(df)

if __name__ == "__main__":
    main()
