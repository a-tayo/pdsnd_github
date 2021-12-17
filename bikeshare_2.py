import time
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = 'January,February,March,April,May,June'.split(',')
days = 'Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday'.split(',')

def get_filters(c = ''):
    """
    Asks user to specify a city, month, and day to analyze.

    Args:
        (str) c - name of the previous city selected if this is not the first run
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #Clearing the screen before starting the program and after each restart 
    if os.name == 'posix': #for mac and linux platforms
       os.system('clear')
    elif os.name == 'nt': #for windows platform
       os.system('cls')
    print('\n\n')
    
    city = c
    choice = ""
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print()
        if not city or choice == 'yes':
            print("Which US city would you like to explore?")
            print("Available cities are Chicago, New York, Washington")
            print()
            city = input().lower()
        
        if city == 'new york':
            city = 'new york city'
        if city not in (list(CITY_DATA.keys())):
            print("No data available for {}".format(city.title()))
        else:
            print("Selected city is {}".format(city.title()))
            print("Would you like to change your city? yes or press Enter to skip?")
            choice = input().lower()
            if choice == 'yes':
                continue
            break

    # get user input for month (all, january, february, ... , june)
    print("Would you like to filter by month? yes or press Enter to skip")
    f_mth = input().lower()
    if f_mth == 'yes':
        print("Which month?")
        print("Month can be one of {}".format(', '.join(months)))
        month = input().title()
        print()
        while month not in months:
            print("{} is not a valid option.".format(month))
            month = input("Which month?").title()
    else:
        month = "all"
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("Would you like to filter by day? yes or press Enter to skip")
    f_day = input().lower()
    if f_day == 'yes':
        print("Which day?")
        print("Day can be one of {}".format(', '.join(days)))
        day = input().title()
        print()
        while day not in days:
            print("{} is not a valid option.".format(day))
            day = input("Which day?").title()
    else:
        day = "all"

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
     #Set up the DataFrame for the selected city and apply the necessary filters   
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    df['Start_End'] = df['Start Station'] + ' ----> ' + df['End Station']

#     filter by month or day or both
    if month != 'all':
        df = df.loc[df['month'] == month]

    if day != 'all':
        df = df.loc[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print()
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month of travel is: {}".format(df['month'].mode().values[0]))

    # display the most common day of week
    print("Most common day of week is: {}".format(df['day'].mode().values[0]))

    # display the most common start hour
    start_hour = df['Start Time'].dt.hour.mode().values[0]
    print("Most common start hour is the {} hour.\n".format(start_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station is: {}'.format(df['Start Station'].mode().values[0]))

    # display most commonly used end station
    print('Most common end station is: {}'.format(df['End Station'].mode().values[0]))

    # display most frequent combination of start station and end station trip
    print('Most common trip (Start to End) is: {}'.format(df['Start_End'].mode().values[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: ', pd.to_timedelta(sum(df['Trip Duration']), unit='s'))

    # display mean travel time
    print('Average travel time is: ',pd.to_timedelta(df['Trip Duration'].mean(), unit='s')) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User counts:")
    print(df['User Type'].value_counts() if 'User Type' in df.columns else "User Type not specified")

    # Display counts of gender
    print("\nGender count:")
    print(df['Gender'].value_counts() if 'Gender' in df.columns else "Gender not specified\n") 

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        print("\nEarliest year of birth: ",int(birth_year.min()))
        print("Most recent year of birth: ",int(birth_year.max()))
        print("Most common year of birth: ",int(birth_year.mode().values[0]))
    else:
        print("Birth Year not specified.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    restart = ""
    while True:
        if not restart:
            city, month, day = get_filters()
            p_city = city
        else:
            city, month, day = get_filters(c = p_city)
            p_city = city
        df = load_data(city, month, day)

        time_stats(df)
        if not input("\nPress Enter to view the next Statistics.."):
            station_stats(df)
        if not input("\nPress Enter to view the next Statistics.."):
            trip_duration_stats(df)
        if not input("\nPress Enter to view the next Statistics.."):
            user_stats(df)
        time.sleep(2)
        
        raw = input("\nWould like to view the raw data? Enter y or n\n")
        n = 0
        df = df.drop(['month', 'day', 'Start_End'], axis=1)
        if raw == 'y':
            i = 5
            k = 0
            while True:
                print()
                if i < max(list(df.index)):
                    while k < i:
                        print()
                        print(df.iloc[k])
                        print()
                        k += 1    
                else:
                    print("No more data.")
                    break
                print()
                i += 5
                if not input("Press Enter to continue or type q to quit.\n"):
                    continue
                else:
                    break
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
