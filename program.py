import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
import data_functions
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Prints model statistics
def ols(data, model, X_vars, Y_var):
    with_constant = sm.add_constant(data[X_vars])

    # Print OLS summary
    regression = sm.OLS(data[Y_var], with_constant).fit()
    print(regression.summary(alpha=0.01))

    # Print VIF
    vif = pd.DataFrame({
        'VIF': [variance_inflation_factor(with_constant.values, i) for i in range(len(with_constant.columns))],
        'Variable': with_constant.columns
    })
    print('\n', vif)
    
    # Do 4-fold cross validation
    scores = cross_val_score(model, data[X_vars], data[Y_var], cv=4)
    print(f'\nCross validation score: {round(scores.mean(), 4)}')

# Projects wRC+ for a single player
def project_player(model, X_vars, Y_var):
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
def project_year(year, model, X_vars, Y_var):
    file_name = f'{year}_{Y_var}_projections.tsv'

    projections = pd.DataFrame()
    to_be_projected = Y_var.split("_")[0] # Remove _curr from the variable name

    data = pd.read_csv(f'./data/batting_{year-1}.tsv', sep='|')

    # For each player, project wRC+ based on their stats
    for player in data['Name']:
        player_data = data[data['Name'] == player]
        input_df = pd.DataFrame({var: player_data[var.replace('_prev', '')].values[0] for var in X_vars}, index=[0])

        projected_y = round(model.predict(input_df)[0])
        projections = pd.concat([projections, pd.DataFrame({'Name': player,
                                                            f'Projected {to_be_projected}': projected_y},
                                                            index=[0])], ignore_index=True)
    
    projections.sort_values(by=f"Projected {to_be_projected}", ascending=False, inplace=True)
    projections.to_csv(file_name, sep='|', index=False)
    print(f"\n{year} projections saved to {file_name}")

def menu():
    choices = {
        "wRC+": ['wRC+', 'Age', 'maxEV', 'LA', 'HardHit%', 'O-Swing%', 'O-Contact%', 'CStr%'],
        "BB%": ['BB%', 'O-Swing%'],
        'K%': ['K%', 'O-Contact%']
    }

    while True:
        print("\nPick a stat to project (or [q]uit):")
        choice = input("> ")

        # Allow entering number instead of stat name for quick testing
        try:
            choice = int(choice)
            choice = list(choices.keys())[choice-1]
        except:
            pass
    
        if choice in choices:
            X_vars = [var + '_prev' for var in choices[choice]]
            Y_var = choice + '_curr'
            break
        elif choice == 'q':
            return
        else:
            print(f'Only {", ".join(choices.keys())} are valid choices.')
            continue

    data_functions.get(2015, 2023)
    print('\nLoading data...')
    data = data_functions.load(2015, 2023)

    print('Training model...')
    model = linear_model.LinearRegression()
    model.fit(data[X_vars], data[Y_var])

    while True:
        print("\nMain Menu (or [q]uit):")
        print("1. Print Model Statistics")
        print(f"2. Project Player {choice}")
        print(f"3. Project 2024 {choice}")
        
        choice = input("> ")
        
        if choice == '1':
            ols(data, model, X_vars, Y_var)
        elif choice == '2':
            project_player(model, X_vars, Y_var)
        elif choice == '3':
            project_year(2024, model, X_vars, Y_var)
        elif choice == 'q':
            return

menu()