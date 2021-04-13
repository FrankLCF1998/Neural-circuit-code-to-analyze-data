# Import necessary library
import math, pandas as pd, numpy as np

# Read csv into pandas dataframe
file_name = "414"
df = pd.read_csv(file_name+".csv")

# Label the first column of original csv file on google drive as 'Bin'
df = df.rename(columns={'Unnamed: 0':'Bin'})
bin_values = df['Bin'].unique()

# Remove 'nan' and '*Missing' string variables in the first column from our desired output
bin_values = [bin_value for bin_value in bin_values if not('nan' in str(bin_value) or 'Missing' in str(bin_value))]

# Get the row with #Bin Group
bin_values_index = []
for bin_value in bin_values:
    bin_value_index = df[df['Bin'] == bin_value].index.tolist()
    bin_values_index.append(bin_value_index)

# Convert nested list to flat list to fit .loc required input
bin_values_index = [bin_value_index for elem in bin_values_index for bin_value_index in elem]

# Label all images with #Bin Gourp
n_turns = len(bin_values_index)-1
n = 0
for n in range(n_turns):
    df.loc[bin_values_index[n]+1:bin_values_index[n+1]-1,'Bin'] = bin_values[n]
    n += 1
df.loc[bin_values_index[-1]:df.index[-1],'Bin'] = bin_values[-1]

# Initilaize 
rows_to_delete = set()
delete_count = 0

# Find bin group with type 3 marker
for bin in bin_values:
    bin_rows = df.loc[df["Bin"] == bin]
    type3_rows_index = bin_rows.index[bin_rows["Type"] == 3].tolist()
    
    # Find closest type 1 marker with same coordinate in same bin group
    for type3_index in type3_rows_index:
        x,y = bin_rows.loc[type3_index]["X"], bin_rows.loc[type3_index]["Y"]
        type1_same_xy_rows_index = bin_rows.index[(bin_rows["X"] == x) & (bin_rows["Y"] == y) & (bin_rows["Type"] == 1)].tolist()

        # Find the type 1 rows with the smallest distance and delete both type 3 and type 1 rows
        if len(type1_same_xy_rows_index) > 0:
            min_type1_index_diff = math.inf
            min_type1_index = None
            for type1_same_xy_row_index in type1_same_xy_rows_index:
                diff = abs(type3_index - type1_same_xy_row_index)
                if diff < min_type1_index_diff:
                    min_type1_index_diff = diff
                    min_type1_index = type1_same_xy_row_index
            rows_to_delete.add(type3_index)
            rows_to_delete.add(min_type1_index)
            delete_count += 2

# Report stats
print("Rows deleted:", delete_count)
print(rows_to_delete)

# Create a new dataframe without deleted type 3 and corresponding type 1 markers
df_filtered = df.drop(list(rows_to_delete))

# Exports the new dataframe into a csv in the same folder
df_filtered.to_csv(file_name+"_out"+".csv", index=False)