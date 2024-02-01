import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
import data_functions
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Prints model statistics
def ols(data, model, X_vars, Y_var):
    with_constant = sm.add_constant(data[X_vars])

    regression = sm.OLS(data[Y_var], with_constant).fit()
    print(regression.summary(alpha=0.01))

    vif = pd.DataFrame({
        'VIF': [variance_inflation_factor(with_constant.values, i) for i in range(len(with_constant.columns))],
        'Variable': with_constant.columns
    })
    print('\n', vif)
    
    scores = cross_val_score(model, data[X_vars], data[Y_var], cv=4)
    print(f'\nCross validation score: {round(scores.mean(), 4)}')

# Projects wRC+ for a single player
def project_player(model, X_vars, Y_var):
    while True:
        inputs = {}

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
    to_be_projected = Y_var.removesuffix('_curr')

    projections = pd.DataFrame()
    data = pd.read_csv(f'./data/batting_{year-1}.tsv', sep='|')

    # For each player, project wRC+ based on their stats
    for player in data['Name']:
        player_data = data[data['Name'] == player]
        input_df = pd.DataFrame({var: player_data[var.replace('_prev', '')].values[0] for var in X_vars}, index=[0])

        if '%' in X_vars[0]:
            projected_y = round(model.predict(input_df)[0],3)
        else:
            projected_y = round(model.predict(input_df)[0])
            
        projections = pd.concat([projections, pd.DataFrame({'Name': player,
                                                            f'Projected {to_be_projected}': projected_y},
                                                            index=[0])], ignore_index=True)
    
    # Save the projections
    file_name = f'{year}_{to_be_projected}_projections.tsv'

    projections.sort_values(by=f"Projected {to_be_projected}", ascending=False, inplace=True)
    projections.to_csv(file_name, sep='|', index=False)
    print(f"\n{year} projections saved to {file_name}")

def menu():
    data_functions.get(2015, 2023)
    print('\nLoading data...')
    data = data_functions.load(2015, 2023)

    variables = {
        "wRC+": ['wRC+', 'Age', 'maxEV', 'LA', 'HardHit%', 'O-Swing%', 'O-Contact%', 'CStr%'],
        "BB%": ['BB%', 'O-Swing%', 'Barrel%', 'ISO'],
        'K%': ['K%', 'Z-Swing%', 'O-Contact%', 'Z-Contact%'],
    }

    while True:
        print("\nPick a stat to project (or [q]uit):")
        choice = input("> ")

        # Allow entering number instead of stat name for quick testing
        try:
            choice = int(choice)
            choice = list(variables.keys())[choice-1]
        except:
            pass
            
        if choice == 'a':
            for stat in variables:
                X_vars = [var + '_prev' for var in variables[stat]]
                Y_var = stat + '_curr'

                print(f'\nTraining model for {stat}...')
                model = linear_model.LinearRegression()
                model.fit(data[X_vars], data[Y_var])

                project_year(2024, model, X_vars, Y_var)
                continue
        elif choice in variables:
            X_vars = [var + '_prev' for var in variables[choice]]
            Y_var = choice + '_curr'
        elif choice == 'q':
            return
        else:
            print(f'Only {", ".join(variables.keys())} are valid choices.')
            continue

        print('\nTraining model...')
        model = linear_model.LinearRegression()
        model.fit(data[X_vars], data[Y_var])

        while True:
            print("\nMain Menu (or [q]uit):")
            print("1. Print Model Statistics")
            print(f"2. Project Player {Y_var.removesuffix('_curr')}")
            print(f"3. Project 2024 {Y_var.removesuffix('_curr')}")
            
            choice = input("> ")
            
            if choice == '1':
                ols(data, model, X_vars, Y_var)
            elif choice == '2':
                project_player(model, X_vars, Y_var)
            elif choice == '3':
                project_year(2024, model, X_vars, Y_var)
            elif choice == 'q':
                break

menu()