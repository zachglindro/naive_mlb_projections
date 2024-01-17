import pybaseball as pb
import pandas as pd
import os

DEFAULT_START_YEAR = 2015
DEFAULT_END_YEAR = 2023
MINIMUM_PA = 300

# Get batter data for the model, minimum 300 PA
def get(start_year=DEFAULT_START_YEAR, end_year=DEFAULT_END_YEAR, exclude_2020=True, force_update=False):
    if not os.path.exists('data'):
        os.mkdir('data')

    for season in range(start_year, end_year+1):
        if season == 2020 and exclude_2020:
            continue
        
        if os.path.exists(f'data/batting_{season}.tsv') and not force_update:
            continue

        print(f'Getting data for {season}...')
        data = pb.batting_stats(season, qual=MINIMUM_PA, ind=1)

        data.to_csv(f'data/batting_{season}.tsv', sep='|')

    return 0

# Loads the data by matching the player names from consecutive seasons
def load(start_year=DEFAULT_START_YEAR, end_year=DEFAULT_END_YEAR):
    pairs = pd.DataFrame()

    # For each season, match the player names with the previous season
    # start_year+1 because we don't need to iterate over the first season
    for season in range(start_year+1, end_year+1):
        try:
            prior = pd.read_csv(f'./data/batting_{season-1}.tsv', sep='|')
            current = pd.read_csv(f'./data/batting_{season}.tsv', sep='|')
        except FileNotFoundError:
            continue

        for player in current['Name']:
            if player in prior['Name'].values:
                # Get the player's data from the previous season and the current season
                player_prior = prior[prior['Name'] == player]
                player_current = current[current['Name'] == player]

                # Rename the columns appropriately
                player_prior.columns = [f'{col}_prev' for col in player_prior.columns]
                player_current.columns = [f'{col}_curr' for col in player_current.columns]

                # Concatenate the dataframes and add to the pairs dataframe
                player_data = pd.concat([player_prior.reset_index(drop=True), player_current.reset_index(drop=True)], axis=1)
                pairs = pd.concat([pairs, player_data], ignore_index=True)

    return pairs