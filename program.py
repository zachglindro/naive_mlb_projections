import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import data

# Variables used for the regression model
X_vars = [ 'wRC+_prev','Barrel%_prev', 'K%_prev', 'BB%_prev', 'Age_prev']
Y_var = 'wRC+_curr'

# Returns the regression model
def start(split=False):

    data.get(2015, 2023)
    print('Loading data...')
    pairs = data.load(2015, 2023)
    print('Training model...')
    regression = linear_model.LinearRegression()

    if split:
        X_train, X_test, y_train, y_test = train_test_split(pairs[X_vars], pairs[Y_var], test_size=0.3, random_state=0)
        regression.fit(X_train, y_train)
        print(f'Score: {regression.score(X_test, y_test)}')
    else:
        regression.fit(pairs[X_vars], pairs[Y_var])

    return regression

# Project wRC+ for a single player
def project_player():
    model = start(split=True)

    while True:
        inputs = {}

        # Ask user for inputs to the X variables
        for var in X_vars:
            inputs[var] = input(f'Enter {var.split("_")[0]}: ')
            if inputs[var] == 'q':
                break
                
            try:
                if '%' in var:
                    inputs[var] = float(inputs[var])/100
                else:
                    inputs[var] = float(inputs[var])
            except ValueError:
                print('Invalid input')
                continue
        
        # Output projected y
        input_df = pd.DataFrame(inputs, index=[0])
        print(f'p{Y_var.split("_")[0]}: {round(model.predict(input_df)[0])}\n')

# Projects wRC+ for each player in the given year
def project_year(year, file_name):
    model = start()
    data = pd.read_csv(f'./data/batting_{year-1}.tsv', sep='|')

    projections = pd.DataFrame()

    for player in data['Name']:
        player_data = data[data['Name'] == player]
        input_df = pd.DataFrame({var: player_data[var.replace('_prev', '')].values[0] for var in X_vars}, index=[0])

        projected_y = round(model.predict(input_df)[0])
        projections = pd.concat([projections, pd.DataFrame({'Name': player,
                                                            f'Projected {Y_var.split("_")[0]}': projected_y},
                                                            index=[0])], ignore_index=True)
    
    projections.to_csv(file_name, sep='|', index=False)
    print(f"{year} projections saved to {file_name}")

#project_player()
project_year(2024, '2024_projections.tsv')