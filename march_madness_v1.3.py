# Import necessary libraries
import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
import sklearn
from sklearn.exceptions import DataConversionWarning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor, MLPClassifier


# Function to fill in missing values in the 'Adj Off Eff' and 'Adj Def Eff' columns of a schedule DataFrame
def kansas_filler():
    # Path to the CSV files
    intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"

    # Read the statistics and schedule CSV files into dictionaries
    stats = pd.read_csv(intro + 'test6_march_madness_2-28.csv', index_col='Rank').to_dict()
    schedule = pd.read_csv(intro + 'kansas23_schedule.csv').to_dict()

    # Display schedule keys
    for i in schedule.keys():
        print(schedule[i])

    # Extract relevant columns from the statistics and schedule dictionaries
    total_eff_off = stats['Adj Off Eff']
    total_eff_def = stats['Adj Def Eff']
    empty_eff_off = schedule['Adj Off Eff']
    empty_eff_def = schedule['Adj Def Eff']

    # Fill in missing values in 'Adj Off Eff' using corresponding values from statistics
    for j in empty_eff_off.keys():
        for i in total_eff_off.keys():
            if i == j:
                empty_eff_off[j] = total_eff_off[i]
            else:
                continue

    # Fill in missing values in 'Adj Def Eff' using corresponding values from statistics
    for j in empty_eff_def.keys():
        for i in total_eff_def.keys():
            if i == j:
                empty_eff_def[j] = total_eff_def[i]

    # Update the 'Adj Off Eff' and 'Adj Def Eff' columns in the schedule dictionary
    schedule['Adj Off Eff'] = empty_eff_off
    schedule['Adj Def Eff'] = empty_eff_def

    # Display lengths and keys of modified columns
    print(len(empty_eff_off))
    print(len(schedule['Team']))

    # Convert schedule and stats dictionaries to DataFrames
    schedule = pd.DataFrame(schedule)
    stats = pd.DataFrame(stats)

    # Uncomment the line below to save the modified schedule DataFrame to a CSV file
    # schedule.to_csv(intro+'kansas23_schedule.csv', mode='w')

    return schedule


# Call the kansas_filler function and print the resulting schedule DataFrame
schedule = kansas_filler()
print(schedule)


# Function to predict team and opponent scores using linear regression and MLP regressor
def kansas_predictor(slate):
    # Define columns used for prediction
    keyglock = ['Team', 'points', 'opp', 'Adj Off Eff', 'Adj Def Eff']
    slatt = slate

    # Extract relevant data for prediction
    teams = slatt[keyglock[0]]
    points = np.array(slatt[keyglock[1]]).reshape(-1, 1)
    opp = np.array(slatt[keyglock[2]]).reshape(-1, 1)
    team_off_eff = np.array(slatt[keyglock[3]]).reshape(-1, 1)
    team_def_eff = np.array(slatt[keyglock[4]]).reshape(-1, 1)

    # Define a function for making predictions using linear regression and MLP regressor
    def predictor(x_train, y_train, x_test):
        num = len(x_train)
        x_train.reshape(-1, 1)
        y_train.reshape(-1, 1)
        x_test = np.array(x_test).reshape(-1, 1)
        y_test = []

        try:
            # Linear Regression
            regr = LinearRegression()
            regr.fit(x_train, y_train)
            y_pred = regr.predict(x_test)
            print("The predicted linear is:", y_pred)

            # MLP Regressor with 'lbfgs' solver
            regr = MLPRegressor(random_state=1, solver='lbfgs', max_iter=500)
            regr.fit(x_train, y_train)
            mlp = regr.predict(x_test)
            print("The predicted neural (lbfgs) is:", mlp)

            # MLP Regressor with 'adam' solver
            regr = MLPRegressor(random_state=1, solver='adam', max_iter=200, learning_rate='adaptive', batch_size=num)
            regr.fit(x_train, y_train)
            mlp = regr.predict(x_test)
            print("The predicted neural (adam) is:", mlp)

            # Append linear and MLP predictions to the y_test list
            y_test.append(y_pred)
            y_test.append(mlp)
        except DataConversionWarning:
            pass

        return y_test

    # Print predicted team and opponent scores
    print('Team Score:', predictor(team_def_eff, points, [int(96)]), '\n\n')
    print('Opponent Score:', predictor(team_off_eff, opp, [int(118)]))


# Call the kansas_predictor function with the schedule DataFrame
kansas_predictor(schedule)
