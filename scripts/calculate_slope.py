# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 15:24:52 2023

This script calculates the slope of the percentage and population
of each country in Sub-Saharan Africa for the following:
    Financial institution account, female (age 15+)
    Mobile money account, female (age 15+)

Each country has a different set of years. If there is only one
year of data, the output is blank.

The output is a csv table named slope_output.csv. The user must
specify an output folder for the results.

@author: Anela Layugan
"""
#### user input ###
# specify an output folder
output_folder = r''
###################

import pandas as pd
import os
import numpy as np

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
    'Adult populaiton'
    ]

## column names of metrics
cols_data = [
        'Financial institution account, female (% age 15+)',
        'Mobile money account, female (% age 15+)'
        ]

cols_all = cols_countries + cols_data

df_subset = subset_data(df, cols_all, 'Sub-Saharan Africa (excluding high income)')

# calculate population for each metric
def calc_pop(df, col):
    new_col=f'{col}_population'
    df[new_col] = df['Adult populaiton'] * df[col]
    return df

cols_pop=[]

for col in cols_data:
    calc_pop(df_subset,col)
    # add to list of cols with population
    cols_pop.append(f'{col}_population')

# combine all columns for slope calculation
cols_data_calc=cols_data+cols_pop

# calculate slope
def calc_slope(df, country, col, output_dict):
    df_country = df.loc[df_subset['Country name']==country]
    if country not in output_dict:
        output_dict[country]=[]
    else:
        pass
    # set default value
    slope_intercept=None
    if col in df_country:
        # set x and y values
        # drop rows that are na
        x = df_country['Year'].dropna()
        y = df_country[col].dropna()
        # calculate if there is more than one year
        if len(y)>1:
        # calculate slope
            idx = np.isfinite(x) & np.isfinite(y)
            slope_intercept = np.polyfit(x[idx], y[idx], 1)
            # add to data dict
            output_dict[country].append(slope_intercept[0])
        else:
            data_dict[country].append(None)
    else:
        data_dict[country].append(None)  
    return output_dict

## list of countries for analysis
countries = df_subset['Country name'].unique()

## empty dict for output
data_dict={}

## run analysis
for country in countries:
    for col in cols_data_calc:
        calc_slope(df_subset,country,col,data_dict)

# output data
## turn into dataframe for output
df = pd.DataFrame.from_dict(data_dict, orient = 'index')

# column names
## combine all columns for output
cols_all = cols_countries + cols_data_calc

df.columns=cols_data_calc
df.index.names=['uniqueID']

# create output
output_name = 'slope_output'
output_fp=os.path.join(output_folder, f'{output_name}.csv')
df.to_csv(output_fp)



