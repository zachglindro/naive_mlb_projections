import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import data

data.get(2015, 2023)
print('Loading data...')
pairs = data.load(2015, 2022)

def startLinear():
    print('\nTraining model...')

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(pairs[['Barrel%_prev', 'wRC+_prev', 'K%_prev', 'BB%_prev', 'Age_prev']], pairs['wRC+_curr'], test_size=0.3, random_state=0)
    
    # Train model
    regression = linear_model.LinearRegression()
    regression.fit(pairs[['Barrel%_prev', 'wRC+_prev', 'K%_prev', 'BB%_prev', 'Age_prev']], pairs['wRC+_curr'])

    print(f'Score: {regression.score(X_test, y_test)}')

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
        print(f'Predicted wRC+: {round(regression.predict(input_df)[0])}')

startLinear()