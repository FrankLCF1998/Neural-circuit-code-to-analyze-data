# Import necessary libraries
import glob
import pandas as pd
import numpy as np

# Define .xlsx filenames
filename_1 = glob.glob('*closed.xlsx')
filename_2 = glob.glob('*open.xlsx')
filename_3 = glob.glob('*in.xlsx')
filename_4 = glob.glob('*out.xlsx')
filename_5 = glob.glob('*coc.xlsx')
filename_6 = glob.glob('*saline.xlsx')
filename_7 = glob.glob('*move.xlsx')
filename_8 = glob.glob('*still.xlsx')
filenames = filename_1 + filename_2 + filename_3 + filename_4 + filename_5 + filename_6 + filename_7 + filename_8
filenames = [filename.replace('.xlsx', '') for filename in filenames]

# Read xlsx into pandas dataframe
# Caluculate and export mean column over all columns to new dataframe
# Calculate mean, max, min, # of events over the dataframe. Export these parameters to a new dataframe
for filename in filenames:
    df = pd.read_excel(filename+'.xlsx', header = None)
    df_filtered_1 = df.mean(axis = 1)
    df_filtered_1.to_excel(filename + '_converted.xlsx', header = False, index = False)
    n = df.shape[1]
    df['# of events'] = n
    df['max Z score'] = max(df.iloc[:, 0:n].max(axis = 1))
    df['min Z score'] = min(df.iloc[:, 0:n].min(axis = 1))
    df['average'] = np.mean(df_filtered_1)
    df_filtered_2 = df[['# of events','max Z score','min Z score','average']]
    df_filtered_2 = df_filtered_2.drop(df_filtered_2.index[1:])
    df_filtered_2 = df_filtered_2.transpose()
    df_filtered_2.to_excel(filename + '_parameter.xlsx', header = False)