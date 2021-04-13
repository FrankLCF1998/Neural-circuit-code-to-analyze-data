# This script returns a .csv with the frame + timestamp each time the mouse crosses zones
# Import necessary libraries
import csv, math, os, numpy as np, seaborn as sns, pandas as pd, matplotlib.pyplot as plt, shapely
from shapely import geometry
from shapely.geometry import Point, Polygon


##### Refactored By Yihan 07-02-2020 ########

# Define csv filenames
filename_1 = 'NAcMedcell-EPMr-200402-091933_11-200402-131527.csv'

# Define EPM coords for open/closed arms 1/2 and center zone
# Polygon makes a polygon from 3+ coords by tracing the coords in given order
# will not work if you jupm from botL->topL->botR->topR
# coordinate system starts with (0,0) in the to-left corner of video
# five zones (4 arms + center) defined by intersection of 8 lines (4x * 4y)
#x1 = 7
x2 = 236
width = 45
x3 = x2 + width
#x4 = 482
#y1 = 3
y2 = 30
height = 34
y3 = y2 + height
#y4 = 331



# Define Center polygon using coords
# Define Center line = boundary line
Center_topL = (x2, y2)
Center_topR = (x3, y2)
Center_botR = (x3, y3)
Center_botL = (x2, y3)
Center = Polygon([Center_botL, Center_topL, Center_topR, Center_botR])
Center_line = geometry.LineString([Center_botL, Center_topL, Center_topR, Center_botR])

##########################################################################################
# Read csv into pandas dataframe
# Convert 'Date' and 'Time' from csv file into dataframe timeseries
df_1 = pd.read_csv(filename_1)
df_1.index = pd.to_datetime(df_1['Date']+ ' ' + df_1['Time'], format="%m/%d/%Y %I:%M:%S %p")
df_1 = df_1.drop(columns=['Date', 'Time'])
df_1 = df_1.astype({'Head X':'float64', 'Head Y':'float64','Body X':'float64','Body Y':'float64','Tail X':'float64','Tail Y':'float64'})

# Drop rows that do not have a coord in either X or Y
df_1 = df_1.loc[df_1['Body X'] != 0.0]
df_1 = df_1.loc[df_1['Head X'] != 0.0]

#Create a new column with tuple (Body X, Body Y)
df_1['Body XY'] = df_1.apply(lambda row: Point(row["Body X"], row["Body Y"]), axis=1)

# Create a new column with tuple (Head X, Head Y)
df_1['Head XY'] = df_1.apply(lambda row: Point(row["Head X"], row["Head Y"]), axis=1)

# The function which_zone categorizes each coordinate into its zone
# OpenArm1 = '0'
# OpenArm2 = '1'
# ClosedArm1 = '2'
# ClosedArm2 = '3'
# Center = '4'
def which_zone(coord):

	if coord.within(Center) or Center_line.contains(coord):
		return '4'
	elif coord.x < x2:
		return '0'
	elif coord.x > x3:
		return '1'
	elif coord.y > y2:
		return '2'
	elif coord.y < y3:
		return '3'

def zone_name(num):
	if num == '0':
		num = 'OpenArm1'
	elif num == '1':
		num = 'OpenArm2'
	elif num == '2':
		num = 'ClosedArm1'
	elif num == '3':
		num = 'ClosedArm2'
	elif num == '4':
		num = 'Center'
	return num

# Creates a new column 'Body Zone' that takes the XY Point coord and finds which zone it lies in
df_1['Body Zone'] = df_1['Body XY'].apply(which_zone)

# Creates a new column 'Body Zone ID' that takes the Body Zone # and assigns it with the name
df_1['Body ZoneID'] = df_1['Body Zone'].apply(zone_name)

# Creates a new column 'Body DiffZone' that returns a non-0 # whenever the zone changes from prev row
df_1['Body DiffZone'] = df_1['Body Zone'].astype(float).diff()

# Creates a new column 'Head Zone' that takes the XY Point coord and finds which zone it lies in
df_1['Head Zone'] = df_1['Head XY'].apply(which_zone)

# Creates a new column 'Head Zone ID' that takes the Head Zone # and assigns it with the name
df_1['Head ZoneID'] = df_1['Head Zone'].apply(zone_name)

# Creates a new column 'Head DiffZone' that returns a non-0 # whenever the zone changes from prev row
df_1['Head DiffZone'] = df_1['Head Zone'].astype(float).diff()

# Creates a new dataframe with just values from when the body zone changes
df_1_filtered = df_1[df_1['Body DiffZone'] != 0]

# Creates a new dataframe with just values from when the head zone changes
# df_1_filtered = df_1[df_1['Head DiffZone'] != 0]

# Creates a new column 'ZoneChange' with zone change info
#df_1_filtered['ZoneChange'] = df_1_filtered['DiffZone'].apply(which_zonechange)

# Exports the new dataframe into a csv in the same folder
df_1_filtered[['No.', 'Body Zone', 'Body ZoneID']].to_csv(filename_1[:-4] + '_zonecross.csv')
