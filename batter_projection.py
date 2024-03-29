"""Functions for projecting wRC+ for a single player or all players in a given year"""
import pandas as pd
from sklearn.model_selection import cross_val_score
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

def ols(data, model, x, y):
    """Prints model statistics"""
    with_constant = sm.add_constant(data[x])

    regression = sm.OLS(data[y], with_constant).fit()
    print(regression.summary(alpha=0.01))

    vif = pd.DataFrame({
        'VIF': [variance_inflation_factor(with_constant.values, i)
                for i in range(len(with_constant.columns))],
        'Variable': with_constant.columns
    })
    print('\n', vif)

    scores = cross_val_score(model, data[x], data[y], cv=4)
    print(f'\nCross validation score: {round(scores.mean(), 4)}')

def project_player(model, x, y):
    """Projects wRC+ for a single player"""
    while True:
        inputs = {}

        for var in x:
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
        print(f'p{y.split("_")[0]}: {round(model.predict(input_df)[0])}\n')

def project_year(year, model, x, y):
    """Projects wRC+ for every player in the given year"""
    to_be_projected = y.removesuffix('_curr')

    projections = pd.DataFrame()
    data = pd.read_csv(f'./data/batting_{year-1}.csv')

    # For each player, project wRC+ based on their stats
    for player in data['Name']:
        player_data = data[data['Name'] == player]
        input_df = pd.DataFrame({var: player_data[var.replace('_prev', '')].values[0] for var in x},
                                index=[0])

        if '%' in x[0]:
            projected_y = round(model.predict(input_df)[0],3)
        else:
            projected_y = round(model.predict(input_df)[0])

        projections = pd.concat([projections,
                                 pd.DataFrame({'Name': player,
                                               f'Projected {to_be_projected}': projected_y},
                                               index=[0])], ignore_index=True)

    # Save the projections
    file_name = f'{year}_{to_be_projected}_projections.csv'

    projections.sort_values(by=f"Projected {to_be_projected}", ascending=False, inplace=True)
    projections.to_csv(f'projections/{file_name}', index=False, quoting=1)
    print(f"\n{year} projections saved to {file_name}")
