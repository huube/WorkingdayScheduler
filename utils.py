import pandas as pd
import numpy as np
from datetime import datetime

def CreateScheduler():
    """This function creates a schedule template for working days. 
    It requires an excel file as input containing each date (defined as 'Date') of a year. 
    including a column 'IsWorkingDay' containing 0 (meaning not a workingday) or 1 (meaning is a workingday).
    This function then transforms this into an output file including a date per workingday per year per month."""

    df = pd.read_excel("workingdays.xlsx") 
    df['Year'] = pd.DatetimeIndex(df['Date']).year ## Add year to group on
    df['Month'] = pd.DatetimeIndex(df['Date']).month ## Add month to group on
    df.set_index(df['Date'],inplace=True) ## set date as index for merge
    del df['Date']

    df_workingdays = df.groupby(['Year','Month'],as_index=False)['IsWorkingDay'].cumsum().reset_index() ## create running sum of working days to get rid of non-workingdays
    df_workingdays.set_index(df_workingdays['Date'],inplace=True) ## set date as index for merge
    del df_workingdays['Date']

    df_unique_workingdays = pd.merge(df, df_workingdays, left_index=True, right_index=True).reset_index() ## merge with input dataframe

    ## fix column naming
    for column in df_unique_workingdays: 
        if '_x' in column:
            df_unique_workingdays.drop(columns=column,inplace=True)
    df_unique_workingdays.columns = df_unique_workingdays.columns.str.replace('_y','')

    ## Get first date for cumulated workingdays. 
    df_workingdays = df_unique_workingdays.groupby(['Year','Month','IsWorkingDay'],sort=True)['Date'].agg("min").reset_index()
    df_workingdays.rename(columns={'IsWorkingDay':'WorkingDay'},inplace=True)

    ## Save results to a file as
    df_workingdays.to_excel('Workingdays_cleansed.xlsx',index=False)    