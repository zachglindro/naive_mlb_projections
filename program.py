from sklearn import linear_model
import data_functions
import batter_projection as bp

def menu():
    data_functions.get(2015, 2023)
    data = data_functions.load(2015, 2023)

    variables = {
        "wRC+": ['wRC+', 'Age', 'maxEV', 'LA', 'HardHit%', 'O-Swing%', 'O-Contact%', 'CStr%'],
        "BB%": ['BB%', 'O-Swing%', 'Barrel%', 'ISO'],
        'K%': ['K%', 'Z-Swing%', 'O-Contact%', 'Z-Contact%'],
    }

    while True:
        print("\nPick [a] stat to project (or [q]uit):")
        choice = input("> ")

        # Allow entering number instead of stat name for quick testing
        try:
            choice = int(choice)
            choice = list(variables.keys())[choice-1]
        except (ValueError, IndexError):
            pass

        if choice == 'a':
            for x, y in variables.items():
                x = [var + '_prev' for var in x]
                y = y + '_curr'

                print(f'\nTraining model for {y}...')
                model = linear_model.LinearRegression()
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
        model = linear_model.LinearRegression()
        model.fit(data[x], data[y])

        while True:
            print("\nMain Menu (or [q]uit):")
            print("1. Print Model Statistics")
            print(f"2. Project Player {y.removesuffix('_curr')}")
            print(f"3. Project 2024 {y.removesuffix('_curr')}")

            choice = input("> ")

            if choice == '1':
                bp.ols(data, model, x, y)
            elif choice == '2':
                bp.project_player(model, x, y)
            elif choice == '3':
                bp.project_year(2024, model, x, y)
            elif choice == 'qq':
                return
            elif choice == 'q':
                break

menu()
