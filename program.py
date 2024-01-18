import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import data
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Variables used for the regression model
X_vars = ['wRC+', 'Age', 'Barrel%', 'HardHit%', 'maxEV', 'O-Swing%', 'O-Contact%', 'CStr%']
Y_var = 'wRC+'

X_vars = [var + '_prev' for var in X_vars]
Y_var = Y_var + '_curr'

# Returns the regression model
def start(split=False, get_pairs=False):
    data.get(2015, 2023)
    print('\nLoading data...')
    pairs = data.load(2015, 2023)
    print('Training model...')
    regression = linear_model.LinearRegression()

    if split:
        X_train, X_test, y_train, y_test = train_test_split(pairs[X_vars], pairs[Y_var], test_size=0.3, random_state=0)
        regression.fit(X_train, y_train)
        print(f'Score: {regression.score(X_test, y_test)}')
    else:
        regression.fit(pairs[X_vars], pairs[Y_var])

    if get_pairs:
        return regression, pairs
    else:
        return regression

# Prints model statistics
def ols():
    regression, pairs = start(split=True, get_pairs=True)
    X = sm.add_constant(pairs[X_vars])
    regression = sm.OLS(pairs[Y_var], X).fit()
    print(regression.summary(alpha=0.01))

    # Get VIF
    vif = pd.DataFrame()
    vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
    vif['Variable'] = X.columns
    print('\n', vif)

# Projects wRC+ for a single player
def project_player():
    model = start()

    while True:
        inputs = {}

        # Ask user for inputs to the X variables
        for var in X_vars:
            inputs[var] = input(f'Enter {var.split("_")[0]}: ')
            if inputs[var] == 'q':
                return
                
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

# Projects wRC+ for every player in the given year
def project_year(year, save_to):
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
    
    projections.to_csv(save_to, sep='|', index=False)
    print(f"{year} projections saved to {save_to}")

def menu():
    while True:
        print("\nMain Menu (or [q]uit):")
        print("1. Print Model Statistics")
        print("2. Project Player wRC+")
        print("3. Project 2024 wRC+")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            ols()
        elif choice == '2':
            project_player()
        elif choice == '3':
            '''year = int(input("Enter the year: "))
            if year < 2015:
                print("\nStatcast data only available from 2015 onwards")
                continue
            save_to = input("Enter the file path to save to: ")'''
            project_year(2024, '2024_projections.tsv')
        elif choice == 'q':
            break

menu()