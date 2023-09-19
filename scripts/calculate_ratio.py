"""
Created on Thu Aug  3 15:24:52 2023

This script calculates the male-to-female ratio of account
ownership for each country in Sub-Saharan Africa for each year of
data for the following metrics:
    Account, {sex} (age 15+)
    Financial institution account, {sex} (age 15+)
    Mobile money account, {sex} (age 15+)

The output is a csv table named ratio_output.csv. The user must
specify an output folder for the results.

@author: Anela Layugan
"""
#### user input ###
# specify an output folder
output_folder = r''
###################

import pandas as pd
import os

# filepath to dataset
data_url = 'https://thedocs.worldbank.org/en/doc/6d8435d479acefaa8960dc85f47efb6a-0430062023/original/DatabankWide.xlsx'

# create dataframe
df = pd.read_excel(data_url,sheet_name = 'Data')

# create subset of data for all ssa countries
def subset_data(df_data,fields,region):
    df_region = df_data.loc[(df_data['Region']==region)]
    df_subset = df_region[fields].copy()
    return df_subset

# lists of columns needed for analysis
## descriptive columns
cols_countries = [
    'Country name',
    'Country code',
    'Year',
    ]

## column names of metrics
cols_data = [
    'Account, male (% age 15+)',
    'Account, female (% age 15+)',
    'Financial institution account, male (% age 15+)',
    'Financial institution account, female (% age 15+)',
    'Mobile money account, male (% age 15+)',
    'Mobile money account, female (% age 15+)'
    ]
cols_all = cols_countries + cols_data

df_subset = subset_data(df,cols_all,'Sub-Saharan Africa (excluding high income)')

# for each metric, calculate the male to female ratio
def calc_ratio(metric,df):
    fld_male = f'{metric}, male (% age 15+)'
    fld_female = f'{metric}, female (% age 15+)'
    ratio_col=f'{metric} ratio'
    df[ratio_col]=df[fld_male]/df[fld_female]
    df.drop(columns = [fld_male,fld_female], inplace = True)
    return df

metrics=[
    'Account',
    'Financial institution account',
    'Mobile money account'
    ]

for metric in metrics:
    calc_ratio(metric,df_subset)

# create output
output_name = 'ratio_output.csv'
output_fp=os.path.join(output_folder, f'{output_name}.csv')
df_subset.to_csv(output_fp, index=False)
