# Import necessary libraries
import glob, openpyxl

# Define csv filenames
filenames = glob.glob('*zonecross.csv')
filenames = [filename.replace('zonecross.csv', '') for filename in filenames]

# Create new empty .xlsx files
# For EPM, use 'closed.xlsx' and 'open.xlsx' as input
# For CPP, use 'coc.xlsx' and 'saline.xlsx' as input
# For OFT, use 'in.xlsx' and 'out.xlsx' as input
for filename in filenames:
    wb = openpyxl.Workbook()
    wb.save(filename + 'closed.xlsx')
    wb.save(filename + 'open.xlsx')
    wb.close()