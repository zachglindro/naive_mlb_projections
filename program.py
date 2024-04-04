from sklearn import linear_model
import data_functions
import batter_projection as bp
import os

def menu():
    model = linear_model.LinearRegression()

    data_functions.get(2015, 2023)
    data = data_functions.load(2015, 2023)

    variables = {
        "wRC+": ['Age', 'BB%', 'K%', 'BABIP', 'SLG', 'EV', 'maxEV', 'LA', 'Barrel%', 'HardHit%', 'xBA', 'GB/FB', 'IFFB%', 'BUH%', 'Pull%', 'Oppo%', 'O-Swing%'],
        "BB%": ['BB%', 'O-Swing%', 'Barrel%', 'ISO'],
        'K%': ['K%', 'Z-Swing%', 'O-Contact%', 'Z-Contact%'],
    }

    while True:
        print("\nPick [a] stat to project (or [q]uit):")
        choice = input("> ")

        try:
            # If the user enters a number, convert it to the corresponding variable
            choice = int(choice)
            choice = list(variables.keys())[choice-1]
        except (ValueError, IndexError):
            pass

        if choice == 'a':
            # Project each variable
            for x, y in variables.items():
                x = [var + '_prev' for var in x]
                y = y + '_curr'

                print(f'\nTraining model for {y}...')
                model.fit(data[x], data[y])

                bp.project_year(2024, model, x, y)
            continue

        if choice in variables:
            x = [var + '_prev' for var in variables[choice]]
            y = choice + '_curr'
        elif choice == 'q':
            return
        else:
            print(f'Only {", ".join(variables.keys())} are valid choices.')
            continue

        print('\nTraining model...')
        model.fit(data[x], data[y])

        while True:
            print("\nMain Menu (or [q]uit):")
            print("1. Print Model Statistics")
            print(f"2. Project 2024 {y.removesuffix('_curr')}")

            choice = input("> ")

            if choice == '1':
                bp.info(data, model, x, y)
            elif choice == '1p':
                directory = f'graphs/{y.split("_")[0]}'

                if not os.path.exists(directory):
                    os.makedirs(directory)
                for file in os.listdir(directory):
                    os.remove(os.path.join(directory, file))

                bp.info(data, model, x, y, print_graphs=True)
            elif choice == '2':
                bp.project_year(2024, model, x, y)
            elif choice == 'qq':
                return
            elif choice == 'q':
                break

menu()
