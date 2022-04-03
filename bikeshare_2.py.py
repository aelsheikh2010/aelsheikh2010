#!/usr/bin/env python
# coding: utf-8

# In[3]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def check_data_entry(prompt, valid_entries): 
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries : 
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input

    except:
        print('Seems like there is an issue with your input')



def get_filters(): 
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hi there! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)


    # get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Please choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # extract hours from start time to creat new coulmn hour
    df['hour'] = df['Start Time'].dt.hour
    
# use the index of the months list to get the corresponding int
    # filter by month if applicable
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month != 'all'and month != '' and month!= None and month in months :
        
        month = months.index(month) + 1 
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        

    # filter by day of week if applicable
    days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    if day != 'all' and day != '' and day!=None  and day in days:
        
        #day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        #print (df['day_of_week'])
        
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    
    print('the most common month = ',popular_month)
    
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    
    print('the most common day of week = ',popular_day)
    
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    
    print('the most common start hour = ',popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_stat = df['Start Station'].mode()[0]
    print('most commonly used start station is: ',popular_start_stat)
    print()
    # display most commonly used end station
    popular_end_stat = df['End Station'].mode()[0]
    print('most commonly used end station is: ',popular_end_stat)
    print()
    # display most frequent combination of start station and end station trip
    output = df.groupby(['Start Station','End Station']).count().sort_values(by=['Start Station','End Station'], axis = 0).iloc[0]
    print('most frequent combination of start station and end station trip is: ',output)
    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_trip=df['Trip Duration'].sum()
    print('total travel time = ',total_time_trip)
    print()
    # display mean travel time
    aver_time_trip=df['Trip Duration'].mean()
    print('mean travel  time = ',aver_time_trip)
    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    count_user_type=df['User Type'].value_counts()
    print('counts of user types: ',count_user_type)
    print()
    # Display counts of gender
    if 'Gender'  in df.columns:
        count_gender=df['Gender'].value_counts()
        print('counts of gender: ',count_gender)
        print()
    else:
        print('No Gender Data in Washington City')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print()
        earliest_birth= df['Birth Year'].min()
        print()
        print('The earliest year of birth is: ',int(earliest_birth))
        print()
        most_recent_birth= df['Birth Year'].max()
        print()
        print('The most recent year of birth is:  ',int(most_recent_birth))
        most_common_birth= df['Birth Year'].mode()
        print()
        print('most common year of birth is: ',int(most_common_birth))
        print()
    
    else:
        print('No Birth Year in Washington City')
        
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):
    """
    ask the user whether he wants to see 5 rows of data each time or not  .

    """
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data=='yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[ ]:





# In[ ]:




