import pandas as pd
import nfl_data_py as nfl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import random

# Function to determine the winner (you need to implement this based on your data)
def determine_winner(row):
    # Placeholder implementation, replace with actual logic
    return row['posteam'] if row['epa'] > 0 else row['defteam']

# Import play-by-play data
years = [2024, 2025]
pbp = nfl.import_pbp_data(years)
pbp_rp = pbp[(pbp['pass'] == 1) | (pbp['rush'] == 1)]
pbp_rp = pbp_rp.dropna(subset=['epa', 'posteam', 'defteam'])

# Ensure the winner column exists
if 'winner' not in pbp_rp.columns:
    pbp_rp['winner'] = pbp_rp.apply(determine_winner, axis=1)

# Example features (you can add more features as needed)
features = ['epa', 'yards_gained', 'air_yards', 'yards_after_catch', 'pass', 'rush']

# Create a target variable (1 if underdog wins, 0 otherwise)
pbp_rp['underdog_win'] = (pbp_rp['posteam'] == pbp_rp['winner']).astype(int)

# Filter relevant columns
data = pbp_rp[features + ['underdog_win']]
data = data.dropna()

X = data[features]
y = data['underdog_win']

# Train the model
model = LogisticRegression()
model.fit(X, y)

# Testing section
# test_years = random.sample(range(2010, 2023), 3)
# accuracies = []

# for year in test_years:
#     train_years = list(range(year - 3, year))
#     pbp_train = nfl.import_pbp_data(train_years)
#     pbp_test = nfl.import_pbp_data([year])
    
#     pbp_train_rp = pbp_train[(pbp_train['pass'] == 1) | (pbp_train['rush'] == 1)]
#     pbp_train_rp = pbp_train_rp.dropna(subset=['epa', 'posteam', 'defteam'])
    
#     pbp_test_rp = pbp_test[(pbp_test['pass'] == 1) | (pbp_test['rush'] == 1)]
#     pbp_test_rp = pbp_test_rp.dropna(subset=['epa', 'posteam', 'defteam'])
    
#     if 'winner' not in pbp_train_rp.columns:
#         pbp_train_rp['winner'] = pbp_train_rp.apply(determine_winner, axis=1)
#     if 'winner' not in pbp_test_rp.columns:
#         pbp_test_rp['winner'] = pbp_test_rp.apply(determine_winner, axis=1)
    
#     pbp_train_rp['underdog_win'] = (pbp_train_rp['posteam'] == pbp_train_rp['winner']).astype(int)
#     pbp_test_rp['underdog_win'] = (pbp_test_rp['posteam'] == pbp_test_rp['winner']).astype(int)
    
#     train_data = pbp_train_rp[features + ['underdog_win']].dropna()
#     test_data = pbp_test_rp[features + ['underdog_win']].dropna()
    
#     X_train = train_data[features]
#     y_train = train_data['underdog_win']
#     X_test = test_data[features]
#     y_test = test_data['underdog_win']
    
#     model.fit(X_train, y_train)
#     y_pred = model.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     accuracies.append(accuracy)
#     print(f'Year: {year}, Accuracy: {accuracy}')

# print(f'Average Accuracy: {sum(accuracies) / len(accuracies)}')