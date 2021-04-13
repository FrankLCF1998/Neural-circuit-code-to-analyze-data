  # Import necessary libraries
import glob
import csv, math, os, numpy as np, pandas as pd

################################################################################################

# Define csv filenames
# For LMS csv filenames with 'saline', input'saline*.csv'
# For LMS csv filenames with 'coc', input'coc*.csv'
all_files = glob.glob('saline*.csv')
all_files = [filename.replace('.csv', '') for filename in all_files]

# Read csv into pandas dataframe
# Remove column 'Date' and 'Time'
# get difference between n+1-th row and n-th row
# overwrite column 'No.' with original value
for filename in all_files:
    df = pd.read_csv(filename+'.csv')
    df['Body X'] = df['Body X'].diff()
    df['Body Y'] = df['Body Y'].diff()
    # Set min value of accepted move displacement
    min_displacement_move = 5

    # Get displacement based on position change
    df['Displacement'] = df.apply(lambda row: math.sqrt((row['Body X'])**2 + (row['Body Y'])**2), axis=1)

    # Get frames of multiple states(still, move, run)
    # For a state taking consecutive frames, remain the first frame
    # Lable these frames with state
    still_rows_index = df.index[(df["Displacement"] < min_displacement_move)].tolist()
    still_rows_index_diff = [y - x for x,y in zip(still_rows_index,still_rows_index[1:])]
    still_rows_to_delete_index = [i for i, x in enumerate(still_rows_index_diff) if x == 1]
    still_rows_to_delete_index = np.array(still_rows_to_delete_index) + 1
    for ele in sorted(still_rows_to_delete_index, reverse = True):  
        del still_rows_index[ele] 
    df.loc[still_rows_index,'State'] = 'Still'

    move_rows_index = df.index[(df["Displacement"] >= min_displacement_move)].tolist()
    move_rows_index_diff = [y - x for x,y in zip(move_rows_index, move_rows_index[1:])]
    move_rows_to_delete_index = [i for i, x in enumerate(move_rows_index_diff) if x == 1]
    move_rows_to_delete_index = np.array(move_rows_to_delete_index) + 1
    for ele in sorted(move_rows_to_delete_index, reverse = True):  
        del move_rows_index[ele] 
    df.loc[move_rows_index,'State'] = 'Move'

    df_filtered = df[df['State'].notna()]

    # Compare one frame with the former frame to get state change
    df_filtered_indexes_1 = df_filtered.index[:].tolist()
    df_filtered_indexes_2 = df_filtered.index[1:].tolist()
    n=0
    for df_filtered_index in df_filtered_indexes_2:
        df_filtered.loc[df_filtered_indexes_2[n],'State change'] = df_filtered.loc[df_filtered_indexes_2[n],'State'] + '_from_' + df_filtered.loc[df_filtered_indexes_1[n],'State']
        n += 1

    # Set min_interval between one still frame and neighboring move frame to identify still frames indicating an accepted still
    min_interval_frame = 200
    df_filtered['Duration'] = df_filtered['No.'].diff()
    df_filtered['Duration'] = df_filtered['Duration'].shift(-1)
    df_filtered_1 = df_filtered[df_filtered['State'] == 'Still'].dropna()

    # Remove those still frames indicating an unaccepted still
    rows_to_delete = df_filtered_1.index[df_filtered_1['Duration'] < min_interval_frame].tolist()
    df_filtered = df_filtered.drop(rows_to_delete)

    # Remove those frames with recursive state and state change after removing those unaccpted still frames
    # Convert 'Date' and 'Time' from csv file into dataframe timeseries
    df_filtered = df_filtered.loc[df_filtered['State'] != df_filtered['State'].shift()]
    df_filtered.index = pd.to_datetime(df_filtered['Date']+ ' ' + df_filtered['Time'], format="%m/%d/%Y %I:%M:%S %p")

    # Exports the new dataframe into a csv in the same folder
    df_filtered[['No.', 'Displacement', 'State', 'State change']].to_csv(filename+'_move_updated_200'+'.csv')