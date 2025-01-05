import pandas as pd
import os
import urllib.request 
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import nfl_data_py as nfl
from PIL import Image

# Import play-by-play data
pbp = nfl.import_pbp_data([2024, 2025]) # import play-by-play data by year (change year to get data for a different year)
pbp.shape # check the dimensions of the dataframe
pbp.head() # display the first few rows of the dataframe

# Filter and clean data
pbp_rp = pbp[(pbp['pass'] == 1) | pbp['rush'] == 1] # filter out non-passing and non-rushing plays
pbp_rp = pbp_rp.dropna(subset=['epa', 'posteam', 'defteam']) # drop rows with missing values
pbp_rp.shape

# Calculate EPA (Expected Points Added)
pass_epa = pbp_rp[(pbp_rp['pass'] == 1)].groupby('posteam')['epa'].mean().reset_index().rename(columns = {'epa' : 'pass_epa'}) # average EPA per pass play
pass_epa.sort_values('pass_epa', ascending = False)

rush_epa = pbp_rp[(pbp_rp['rush'] == 1)].groupby('posteam')['epa'].mean().reset_index().rename(columns = {'epa' : 'rush_epa'}) # average EPA per rush play
pass_epa.sort_values('pass_epa', ascending = False)

epa = pd.merge(pass_epa, rush_epa, on = 'posteam') # merge the two dataframes

# Import and process team logos
logos = nfl.import_team_desc()[['team_abbr', 'team_logo_espn']] # import team logos
logo_paths = []
team_abbr = []

if not os.path.exists('logos'): # create a directory to store the logos
    os.makedirs('logos')
    
for team in range(len(logos)): # download and resize team logos
    logo_path = f'logos/{logos["team_abbr"][team]}.tif'
    urllib.request.urlretrieve(logos['team_logo_espn'][team], logo_path)
    
    with Image.open(logo_path) as img:
        img = img.resize((500, 500))  # Resize to 500x500 pixels or any desired size
        img.save(logo_path)
    
    logo_paths.append(logo_path)
    team_abbr.append(logos['team_abbr'][team])

data = {'team_abbr' : team_abbr, 'logo_path' : logo_paths} 
logo_data = pd.DataFrame(data) # create a dataframe with team abbreviations and logo paths

epa_with_logos = pd.merge(epa, logo_data, left_on = 'posteam', right_on = 'team_abbr') # merge the EPA dataframe with the logo dataframe

# Plotting
plt.rcParams['figure.figsize'] = [10, 7] # set the figure size
plt.rcParams['figure.autolayout'] = True # automatically adjust the layout

def getImage(path):
    return OffsetImage(plt.imread(path, format = 'tif'), zoom = 0.08)

x = epa_with_logos['pass_epa']
y = epa_with_logos['rush_epa']
paths = epa_with_logos['logo_path']

fig, ax = plt.subplots(figsize = (10, 7))

for x0, y0, path in zip(x, y, paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon = False)
    ax.add_artist(ab)
    
plt.xlim(-0.2, 0.3)
plt.ylim(-0.25, 0.15)
plt.title('Rush and Pass EPA by Team')
plt.xlabel('Pass EPA')
plt.ylabel('Rush EPA')
#plt.show()

# Calculate and display receiver YAC (Yards After Catch)
receiver_yac = pbp_rp[(pbp_rp['pass'] == 1)].groupby('receiver_player_name').agg({'pass' : 'count', 'yards_after_catch' : 'sum'}).reset_index().rename(columns = {'pass' : 'targets', 'yards_after_catch' : 'yac'}) # calculate the number of targets and total YAC for each receiver
receiver_yac = receiver_yac[(receiver_yac['targets'] >= 100)]
receiver_yac.sort_values('yac', inplace = True)
# print(pbp_rp.columns)
# print(receiver_yac)

receiver_name = receiver_yac['receiver_player_name']
yac = receiver_yac['yac']

fig, ax = plt.subplots(figsize = (10, 7))

ax.barh(receiver_name, yac)
ax.set_title("Yards After Catch, 2024")
ax.set_xlabel("Yards After Catch")
plt.show()