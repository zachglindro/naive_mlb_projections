import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import data

# TODO: add PA as ballast
# Returns the regression model
def start(split=True):
    data.get(2015, 2023)
    print('Loading data...')
    pairs = data.load(2015, 2023)

    print('\nTraining model...')
    regression = linear_model.LinearRegression()

    if split:
        X_train, X_test, y_train, y_test = train_test_split(pairs[['Barrel%_prev', 'wRC+_prev', 'K%_prev', 'BB%_prev', 'Age_prev']], pairs['wRC+_curr'], test_size=0.3, random_state=0)
        regression.fit(X_train, y_train)
        print(f'Score: {regression.score(X_test, y_test)}')
    else:
        regression.fit(pairs[['Barrel%_prev', 'wRC+_prev', 'K%_prev', 'BB%_prev', 'Age_prev']], pairs['wRC+_curr'])

    return regression

def tui():
    model = start()

    # Predict wRC+ based on user input
    while True:
        wrc = input('\nEnter wRC+: ')
        if wrc == 'q':
            break
        barrel = input('Enter Barrel%: ')
        k = input('Enter K%: ')
        bb = input('Enter BB%: ')
        age = input('Enter age: ')

        try:
            barrel = float(barrel)/100
            wrc = float(wrc)
            k = float(k)/100
            bb = float(bb)/100
            age = float(age)
        except ValueError:
            print('Invalid input')
            continue

        input_df = pd.DataFrame({'Barrel%_prev': barrel, 'wRC+_prev': wrc, 'K%_prev': k, 'BB%_prev': bb, 'Age_prev': age}, index=[0])
        print(f'Predicted wRC+: {round(model.predict(input_df)[0])}')

# Project wRC+ for 2024 for each player
def project2024():
    model = start(split=False)
    d23 = pd.read_csv(f'./data/batting_2023.tsv', sep='|')

    projections = pd.DataFrame()

    for player in d23['Name']:
        barrel = d23[d23['Name'] == player]['Barrel%'].values[0]
        wrc = d23[d23['Name'] == player]['wRC+'].values[0]
        k = d23[d23['Name'] == player]['K%'].values[0]
        bb = d23[d23['Name'] == player]['BB%'].values[0]
        age = d23[d23['Name'] == player]['Age'].values[0]

        input_df = pd.DataFrame({'Barrel%_prev': barrel, 'wRC+_prev': wrc, 'K%_prev': k, 'BB%_prev': bb, 'Age_prev': age}, index=[0])
        print(f'{player}: {round(model.predict(input_df)[0])}')
        projections = pd.concat([projections, pd.DataFrame({'Name': player, 'wRC+': round(model.predict(input_df)[0])}, index=[0])], ignore_index=True)
    
    projections.to_csv('2024_projections.tsv', sep='|', index=False)

project2024()