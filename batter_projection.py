"""Functions for projecting wRC+ for a single player or all players in a given year"""
import pandas as pd
from sklearn.model_selection import cross_val_score
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt

def info(data, model, x, y, print_graphs=False):
    """Print model summary, VIF, and (optionally) scatter plots"""
    with_constant = sm.add_constant(data[x])

    # Fit regression model
    regression = sm.OLS(data[y], with_constant).fit()
    print(regression.summary())

    # Calculate VIF
    vif = pd.DataFrame({
        'VIF': [variance_inflation_factor(with_constant.values, i)
                for i in range(len(with_constant.columns))],
        'Variable': with_constant.columns
    })
    print('\n', vif)

    # Perform cross validation
    scores = cross_val_score(model, data[x], data[y], cv=4)
    print(f'\nCross validation score: {round(scores.mean(), 4)}')

    # Print scatter plots of each variable against y
    if print_graphs:
        print('\nGenerating scatter plots...')
        for var in x:
            plt.scatter(data[var], data[y])
            plt.xlabel(var)
            plt.ylabel(y)

            if "/" in var:
                var = var.replace("/", "_")
            plt.savefig(f'graphs/{y.split("_")[0]}/{var.split("_")[0]}.png')

            plt.close()

def project_year(year, model, x, y):
    """Project y for each player in a given year"""
    to_be_projected = y.removesuffix('_curr')

    projections = pd.DataFrame()
    data = pd.read_csv(f'./data/batting_{year-1}.csv')

    # For each player, project y based on their stats
    for player in data['Name']:
        player_data = data[data['Name'] == player]
        input_df = pd.DataFrame({var: player_data[var.replace('_prev', '')].values[0] for var in x},
                                index=[0])

        # Round y to nearest integer unless it's a percentage
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
