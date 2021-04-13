# Import necessary libraries
import glob
import pandas as pd

# Define .csv filenames
filenames = glob.glob('*zonecross.csv')
filenames = [filename.replace('.csv', '') for filename in filenames]

# Read csv into pandas dataframe
# For EPM, column name is 'Body ZoneID' and match string is 'Closed' and 'Open'
for filename in filenames:
    df = pd.read_csv(filename+'.csv')
    df_filtered = df[df['Body ZoneID'].str.match('Closed')]
    df_filtered = df_filtered.append(df[df['Body ZoneID'].str.match('Open')])
    df_filtered.to_csv(filename + '_sorted.csv', index = False)