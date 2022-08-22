'''
TODO: create stat file(s) with quality metrics
    1. which SRR#s are different between dbGaP and eutils
    2. which column headers contain duplicate data
    3. which column headers are unique/missing from either eutils or dbGap source
'''
import pandas as pd
import numpy as np

### Import paths
dbgap_file_path='/Users/jdorsheimer/Projects/BDCat/dbGaP-23523/SRA_phs000571/merge_compare/dbGaP_SRARunTable.csv'
eutils_file_path='/Users/jdorsheimer/Projects/BDCat/dbGaP-23523/SRA_phs000571/merge_compare/eutils_SRARunTable.csv'

### Extract header values
dbgap_header = list(pd.read_csv(dbgap_file_path,nrows=0))
eutils_header = list(pd.read_csv(eutils_file_path,nrows=0))

### Create data frames from csv files with headers and sort alphanumerically by SRR#s
dbgap_data = pd.read_csv(dbgap_file_path,header=0,names=dbgap_header).sort_values(by=dbgap_header[0])
eutils_data = pd.read_csv(eutils_file_path,header=0,names=eutils_header).sort_values(by=eutils_header[0])

### Remove empty and zeros columns
dbgap_data = dbgap_data.replace(0,np.nan).dropna(axis=1,how='all')
eutils_data = eutils_data.replace(0,np.nan).dropna(axis=1,how='all')

### Extract first column (SRR#s) from data frames
dbgap_run_list = dbgap_data[dbgap_header[0]].tolist()
eutils_run_list = eutils_data[eutils_header[0]].tolist()

### Select a random SRR# that will be used as a sample to compare data between dbgap and eutils
### Note: the value here could be any SRR#, not just the first one, but the first was chosen for simplicity
sample_id = dbgap_data.iloc[0][0]

### Extract rows corresponding to 'sample_id' in both dbgap and eutils data frames into lists
dbgap_unique_values = dbgap_data.loc[dbgap_data[dbgap_header[0]]==sample_id].values.tolist()[0]
eutils_unique_values = eutils_data.loc[eutils_data[eutils_header[0]]==sample_id].values.tolist()[0]

### Create dictionary for pairing keys and values (data and headers)
temp_dict = {}
### Reselect headers based on removed empty and zeros columns
dbgap_header = list(dbgap_data)
eutils_header = list(eutils_data)
### Create combined lists for headers and data for the above selected SRR#
temp_comb_headers = dbgap_header+eutils_header
temp_comb_unique_values = dbgap_unique_values+eutils_unique_values

### Update dictionary with key:value pairs for data:headers
### This format was chosen because unique data values will only be selected once,
###     whereas headers could be selected multiple times given the nature of the data
for i in range(0,len(temp_comb_headers)):
    if temp_comb_unique_values[i] not in temp_dict:
        temp_dict.update({temp_comb_unique_values[i]: temp_comb_headers[i]})
### Reverse dictionary such that the key:value pairs are now set as headers:data
true_form_dict = {v: k for k, v in temp_dict.items()}

### Extract the headers from temp_dict into a list
stripped_headers = []
for key in true_form_dict.keys():
    stripped_headers.append(key)

### Create new dictionary to hold data for specified column headers
stripped_dict = {}
### Add data to dictionary for specified non-duplicated columns
for header in stripped_headers:
    if header in dbgap_header:
        stripped_dict.update({header: list(dbgap_data[header])})
    elif header in eutils_header:
        stripped_dict.update({header: list(eutils_data[header])})

### Convert dictionary back into data frame
combined_data = pd.DataFrame(stripped_dict)
### Export data from into csv
combined_data.to_csv(r'/Users/jdorsheimer/Projects/BDCat/dbGaP-23523/SRA_phs000571/merge_compare/combined_SRARunTable.csv', index=False, header=True)
