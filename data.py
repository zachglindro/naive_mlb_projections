import pybaseball as pb
import pandas as pd
import os

DEFAULT_START_YEAR = 2015
DEFAULT_END_YEAR = 2023

# Get wRC+ and Barrel% data
def get(start_year=DEFAULT_START_YEAR, end_year=DEFAULT_END_YEAR, exclude_2020=True, force_update=False):
    if not os.path.exists('data'):
        os.mkdir('data')

    for season in range(start_year, end_year+1):
        if season == 2020 and exclude_2020:
            continue
        
        if os.path.exists(f'data/batting_{season}.csv') and not force_update:
            continue

        print(f'Getting data for {season}...')
        data = pb.batting_stats(season, qual=300, ind=1)

        data.to_csv(f'data/batting_{season}.csv', index=False, sep='|')

    return 0

# Load data from the csv files
def load(start_year=DEFAULT_START_YEAR, end_year=DEFAULT_END_YEAR):
    pairs = pd.DataFrame()

    # Match player pairs from consecutive seasons
    # start_year is added 1 because we don't need to iterate over the first season (no prior data)
    for season in range(start_year+1, end_year+1):
        try:
            prior = pd.read_csv(f'./data/batting_{season-1}.csv', sep='|')
            current = pd.read_csv(f'./data/batting_{season}.csv', sep='|')
        except FileNotFoundError:
            continue

        for player in current['Name']:
            if player in prior['Name'].values:
                pairs = pd.concat([pairs, pd.DataFrame({'Name': player,
                                                'Barrel%_prev': prior[prior['Name'] == player]['Barrel%'].values[0],
                                                'wRC+_prev': prior[prior['Name'] == player]['wRC+'].values[0],
                                                'K%_prev': prior[prior['Name'] == player]['K%'].values[0],
                                                'BB%_prev': prior[prior['Name'] == player]['BB%'].values[0],
                                                'Age_prev': prior[prior['Name'] == player]['Age'].values[0],

                                                'wRC+_curr': current[current['Name'] == player]['wRC+'].values[0],},
                                                index=[0])], ignore_index=True)

    return pairs