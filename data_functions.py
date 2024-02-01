import pybaseball as pb
import pandas as pd
import os
from tqdm import tqdm

DEFAULT_START_YEAR = 2015
DEFAULT_END_YEAR = 2023
MINIMUM_PA = 300

# Get batter data for the model, minimum 300 PA
def get(start_year=DEFAULT_START_YEAR, end_year=DEFAULT_END_YEAR, exclude_2020=True, force_update=False):
    if not os.path.exists('data'):
        os.mkdir('data')

    for season in tqdm(range(start_year, end_year+1), desc='Getting data'):
        if season == 2020 and exclude_2020:
            continue
        
        if os.path.exists(f'data/batting_{season}.csv') and not force_update:
            continue

        data = pb.batting_stats(season, qual=MINIMUM_PA, ind=1)
        data.to_csv(f'data/batting_{season}.csv')

# Matches the player names from consecutive seasons.
# Output is a dataframe with the data from the previous season and the current season
def load(start_year=DEFAULT_START_YEAR, end_year=DEFAULT_END_YEAR):
    data = pd.DataFrame()

    # For each season, match the player names with the previous season
    # start_year+1 because we don't need to iterate over the first season
    for season in tqdm(range(start_year+1, end_year+1), desc='Loading data'):
        try:
            prior = pd.read_csv(f'./data/batting_{season-1}.csv')
            current = pd.read_csv(f'./data/batting_{season}.csv')
        except FileNotFoundError:
            continue

        for player in current['Name']:
            if player in prior['Name'].values:
                # Get the player's data from the previous season and the current season
                player_prior = prior[prior['Name'] == player]
                player_current = current[current['Name'] == player]

                # Rename the columns
                player_prior.columns = [f'{col}_prev' for col in player_prior.columns]
                player_current.columns = [f'{col}_curr' for col in player_current.columns]

                # Concatenate the dataframes
                player_data = pd.concat([player_prior.reset_index(drop=True), player_current.reset_index(drop=True)], axis=1)
                data = pd.concat([data, player_data], ignore_index=True)

    return data