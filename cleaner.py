import pandas as pd
import numpy as np
import calendar
import zipfile as zipfile

def zip_to_df(zip_path):
    
    zf = zipfile.ZipFile(zip_path, mode='r')
    mdf = pd.DataFrame()
    
    # Iterate through files in zip file
    for zipfilename in zf.namelist():

        # Read contents of the file and append to mdf
        df = pd.read_csv(zf.open(zipfilename))
        df['departure_date'] = zipfilename[-28:-18]

        mdf = mdf.append(df)

    zf.close() #close zip file
    
    return mdf

def df_dict_compiler(zip_path_list):

    df_dict = {} # Dictionary used to store all the dataframes
    
    for path in zip_path_list:
        df = zip_to_df(path) # Call zip function
        df = df_cleaner(df) # Call data cleaner function
        df_dict[path[5:15]] = df
    
    return df_dict

def df_compiler(zip_path_list):
    
    df_dict = df_dict_compiler(zip_path_list) # Assign df_dict
    mdf = pd.DataFrame() # Instantiate a dataframe to append to
    
    # Iterate through dataframes in df_dict
    for df in df_dict.values():
        mdf = mdf.append(df) # Append each dataframe to mdf
    
    mdf = mdf.astype({'Out Stops':'int', 'Return Stops': 'int', 'Price': 'int', 'total_stops': 'int'})
    mdf.drop_duplicates(inplace=True) # Remove any duplicates
    mdf = mdf.drop('Unnamed: 0', axis=1) # Drop Unnamed column which only populated on Thailand Flight data
    return mdf

def total_duration(df):
    
    out_total = []
    ret_total = []
    # Iterate through 'Out Duration' and 'Return Duration'
    for dur in df['Out Duration']:
        hr = int(dur.split('h')[0]) * 60 # Pull hours and convert to minutes 
        m = int(dur.split('h')[1][:-1]) # Pull minutes
        total = hr + m # Combine both for to
        out_total.append(total)

    for dur in df['Return Duration']:
        hr = int(dur.split('h')[0]) * 60 # Pull hours and convert to minutes 
        m = int(dur.split('h')[1][:-1]) # Pull minutes
        total = hr + m # Combine both for to
        ret_total.append(total)
    # Create a new column with the sum of both    
    df['total_duration'] = pd.Series(out_total) + pd.Series(ret_total)
    
    return df

def dep_ret_time(df):
    # Create lists with only the hours in the time
    dep_times = [time.split(' ')[0] for time in df['Out Time']]
    ret_times = [time.split(' ')[0] for time in df['Return Time']]
    record_time = [time.split('-')[1][:2] for time in df['timestamp']]
    
    df['dep_time'] = pd.Series(dep_times)
    df['ret_time'] = pd.Series(ret_times)
    df['record_time'] = pd.Series(record_time)
    
    return df

def dep_ret_airline(df):
    # Create lists with only the departing airline
    # Remove the layover airlines
    dep_air = [airline.split(',')[0] for airline in df['Out Airline']]
    ret_air = [airline.split(',')[0] for airline in df['Return Airline']]
    
    df['dep_airline'] = pd.Series(dep_air)
    df['ret_airline'] = pd.Series(ret_air)
    
    return df

def name_date_extractor(df):
    # Extract the day of the week each result was searched and each departure date
    dep_day = [calendar.day_name[pd.to_datetime(date).weekday()] for date in df['departure_date']]
    search_day = [calendar.day_name[pd.to_datetime(date).weekday()] for date in df['timestamp']]

    df['departure_day'] = pd.Series(dep_day)
    df['search_day'] = pd.Series(search_day)
    
    return df

def target_assigner(df):
    # Assign targets based on price and total duration time
    # Specifically flights in the bottom 25% of the entire dataframe
    min_price = df['Price'].min()

    mid_price = df['Price'].describe()['25%']
    mid_duration = df['total_duration'].describe()['25%']

    df['target'] = np.where( ( (df['Price'] < mid_price) & (df['total_duration'] < mid_duration) ), 1, 0)
    
    return df

def df_cleaner(df):
    # Pass dataframe through data cleaning process and return cleaned dataframe
    df_duration = total_duration(df)
    
    df_times = dep_ret_time(df_duration)
    
    df_airlines = dep_ret_airline(df_times)
    
    df_date_names = name_date_extractor(df_airlines)
    
    df_date_names['total_stops'] = df['Out Stops'] + df['Return Stops']
    
    dfc = target_assigner(df_date_names)
    
    return dfc