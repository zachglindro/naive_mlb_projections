import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import data

X_vars = [ 'wRC+_prev','Barrel%_prev', 'K%_prev', 'BB%_prev', 'Age_prev']

# Returns the regression model
def start(split=True):

    data.get(2015, 2023)
    print('Loading data...')
    pairs = data.load(2015, 2023)

    print('\nTraining model...')
    regression = linear_model.LinearRegression()

    if split:
        X_train, X_test, y_train, y_test = train_test_split(pairs[X_vars], pairs['wRC+_curr'], test_size=0.3, random_state=0)
        regression.fit(X_train, y_train)
        print(f'Score: {regression.score(X_test, y_test)}')
    else:
        regression.fit(pairs[X_vars], pairs['wRC+_curr'])

    return regression

# Project wRC+ for a single player
def project_player():
    model = start()

    while True:
        inputs = {}

        # Ask user for inputs to the X variables
        for var in X_vars:
            stripped_var = var.split('_')[0]
            inputs[var] = input(f'Enter {stripped_var}: ')
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
        
        # Output projected wRC+
        input_df = pd.DataFrame(inputs, index=[0])
        print(f'pwRC+: {round(model.predict(input_df)[0])}')


'''# Projects 2024 wRC+ for each player
def project2024():
    X_vars = ['wRC+_prev', 'Barrel%_prev', 'K%_prev', 'BB%_prev', 'Age_prev']

    model = start(split=False)
    d23 = pd.read_csv(f'./data/batting_2023.tsv', sep='|')

    projections = pd.DataFrame()

    for player in d23['Name']:
        player_data = d23[d23['Name'] == player]

        input_df = pd.DataFrame({var: player_data[var].values[0] for var in X_vars}, index=[0])

        projections = pd.concat([projections, pd.DataFrame({'Name': player,
                                                            'wRC+': round(model.predict(input_df)[0])},
                                                            index=[0])], ignore_index=True)
    
    projections.to_csv('2024_projections.tsv', sep='|', index=False)'''

# Projects 2024 wRC+for each player
def project2024():
    X_vars = [ 'wRC+_prev','Barrel%_prev', 'K%_prev', 'BB%_prev', 'Age_prev']

    model = start(split=False)
    d23 = pd.read_csv('./data/batting_2023.tsv', sep='|')

    projections = pd.DataFrame()

    for player in d23['Name']:
        barrel = d23[d23['Name'] == player]['Barrel%'].values[0]
        wrc = d23[d23['Name'] == player]['wRC+'].values[0]
        k = d23[d23['Name'] == player]['K%'].values[0]
        bb = d23[d23['Name'] == player]['BB%'].values[0]
        age = d23[d23['Name'] == player]['Age'].values[0]

        input_df = pd.DataFrame({'Barrel%_prev': barrel,
                                 'wRC+_prev': wrc,
                                 'K%_prev': k,
                                 'BB%_prev': bb,
                                 'Age_prev': age}, index=[0])
        
        projections = pd.concat([projections, pd.DataFrame({'Name': player,
                                                            'wRC+': round(model.predict(input_df)[0])},
                                                            index=[0])], ignore_index=True)
    
    projections.to_csv('2024_projections.tsv', sep='|', index=False)

project_player()