# Import necessary libraries
import glob
import pandas as pd

# Define .csv filenames
filenames = glob.glob('*zonecross.csv')
filenames = [filename.replace('.csv', '') for filename in filenames]

# Read csv into pandas dataframe
# For CPP, column name is 'ZonecChange' and match string is 'bottom' and 'top'
# For OFT, column name is 'ZonecChange' and match string is 'in' and 'out'
for filename in filenames:
    df = pd.read_csv(filename+'.csv')
    df = df.iloc[1:]
    df_filtered = df[df['ZoneChange'].str.match('in')]
    df_filtered = df_filtered.append(df[df['ZoneChange'].str.match('out')])
    df_filtered.to_csv(filename + '_sorted.csv', index = False)