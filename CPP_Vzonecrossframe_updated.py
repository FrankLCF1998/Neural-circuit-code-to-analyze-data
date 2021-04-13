# This script returns a .csv with the frame + timestamp each time the mouse crosses zones

# Import necessary libraries
import csv, math, os, numpy as np, seaborn as sns, pandas as pd, matplotlib.pyplot as plt

################################################################################################

# Define csv filenames
filename_1 = 'NAcMed-posttest-200314-080755_c2-7a-200314-101818.csv'

# Define CPP box video coordinates for middle zone
# Biobserve gives coordinates for: Left, Top, Width, Heighcsb
mid_min_x = 195
width = 90
mid_max_x = mid_min_x + width
mid_min_y = 182
height = 16
mid_max_y = mid_min_y + height

# Is the CPP box oriented horizontally or vertically?
# Enter 'horizontal' or 'vertical'
orientation = 'vertical'

#####################################################NAcMed-pretest-200311-082232_c1-2b-200311-090602_Cam1###########################################

# Read csv into pandas dataframe
df_1 = pd.read_csv(filename_1)
df_1 = df_1.astype({'Head X':'float64', 'Head Y':'float64','Body X':'float64','Body Y':'float64','Tail X':'float64','Tail Y':'float64'})

# The function which_zone categorizes each coordinate into its zone
# If zones are stacked vertically in y direction:
# Top zone = '-1'
# Middle zone = '0'
# Bottom zone = '2'
# If zones are stacked horizontally in x direction:
# Right zone = '2'
# Middle zone = '0'
# Left zone = '-1'
def which_zone_x(x_coord):
	if x_coord >= mid_min_x and x_coord <= mid_max_x:
		return '0'
	elif x_coord > mid_max_x:
		return '2'
	elif x_coord < mid_min_x:
		return '-1'

def which_zone_y(y_coord):
	if y_coord >= mid_min_y and y_coord <= mid_max_y:
		return '0'
	elif y_coord > mid_max_y:
		return '2'
	elif y_coord < mid_min_y:
		return '-1'

# Creates a new column 'Zone' that bins the mouse into a zone using x or y coordinate
if orientation == 'horizontal':
	df_1['Zone'] = df_1['Body X'].apply(which_zone_x)
elif orientation == 'vertical':
	df_1['Zone'] = df_1['Body Y'].apply(which_zone_y)

# Creates a new column 'DiffZone' that returns a non-0 # whenever the zone changes from prev row
# To TOP from MIDDLE: 2 - 0 = 2
# To TOP from BOTTOM: 2 - (-1) = 3
# To MIDDLE from BOTTOM: 0 - (-1) = 1
# To MIDDLE from TOP: 0 - 2 = -2
# To BOTTOM from MIDDLE: -1 - 0 = -1
# To BOTTOM from TOP: -1 - 2 = -3
df_1['DiffZone'] = df_1['Zone'].astype(float).diff()

# The function which_zonechange categorizes the type of zone change - HORIZONTAL
def which_zonechange_x(delta):
	if delta == 2:
		return 'right_from_middle'
	elif delta ==3:
		return 'right_from_left'
	elif delta == 1:
		return 'middle_from_left'
	elif delta == -2:
		return 'middle_from_right'
	elif delta == -1:
		return 'left_from_middle'
	elif delta == -3:
		return 'left_from_right'

# The function which_zonechange categorizes the type of zone change - VERTICAL
def which_zonechange_y(delta):
	if delta == 2:
		return 'bottom_from_middle'
	elif delta ==3:
		return 'bottom_from_top'
	elif delta == 1:
		return 'middle_from_top'
	elif delta == -2:
		return 'middle_from_bottom'
	elif delta == -1:
		return 'top_from_middle'
	elif delta == -3:
		return 'top_from_bottom'

# Creates a new dataframe with just values from when the zone changes
df_1_filtered = df_1[df_1['DiffZone'] != 0]

# Creates a new column 'ZoneChange' with zone change info
if orientation == 'horizontal':
	df_1_filtered['ZoneChange'] = df_1_filtered['DiffZone'].apply(which_zonechange_x)
elif orientation == 'vertical':
	df_1_filtered['ZoneChange'] = df_1_filtered['DiffZone'].apply(which_zonechange_y)

# Create a filter
# Input can be  'right_from_middle', 'right_from_left', 'middle_from_left', 'middle_from_right', 'left_from_middle', 'left_from_right' if orientation == horizontal
# 				'bottom_from_middle', 'bottom_from_top', 'middle_from_top', 'middle_from_bottom',  'top_from_middle', 'top_from_bottom' if orientation == vertical
# Output will be all possible combinations of words that you input. Ex: 'bottom_from_top' is equivalent to both 'bottom_from_top' and 'top_from_bottom', so is 'top_from_bottom'
string = '_'.join(sorted(('bottom_from_top').split('_')))

# Normalize values in Column 'ZoneChange' 
df_2_filtered = df_1_filtered.fillna(value = 'NaN')
df_2_filtered['ZoneChange'] = df_2_filtered['ZoneChange'].apply(lambda x: '_'.join(sorted(x.split('_'))))

# Get index of rows we want to remove
turns = df_2_filtered.shape[0]-2
rows_to_delete = []
index = df_2_filtered.index.tolist()

for n in range(turns):
	if df_2_filtered.iloc[n, 11] == string:
		n += 1
		if df_2_filtered.iloc[n, 11] == df_2_filtered.iloc[n+1, 11] and df_2_filtered.iloc[n+1, 11] == df_2_filtered.iloc[n+2, 11]:
			rows_to_delete.append(index[n+1])
			rows_to_delete.append(index[n+2])
	else:
		if df_2_filtered.iloc[n, 11] == df_2_filtered.iloc[n+1, 11] and df_2_filtered.iloc[n+1, 11] == df_2_filtered.iloc[n+2, 11]:
			rows_to_delete.append(index[n+2])

# Avoid duplicate elements
# Remove rows based on index from rows_to_delete
rows_to_delete = list(set(rows_to_delete))
df_1_filtered = df_1_filtered.drop(rows_to_delete)

# Convert 'Date' and 'Time' from csv file into dataframe timeseries
df_1_filtered.index = pd.to_datetime(df_1_filtered['Date']+ ' ' + df_1_filtered['Time'], format="%m/%d/%Y %I:%M:%S %p")
df_1_filtered = df_1_filtered.drop(columns=['Date', 'Time'])

# Exports the new dataframe into a csv in the same folder
df_1_filtered[['No.', 'Zone', 'ZoneChange']].to_csv(filename_1[:-4] + '_zonecross.csv')