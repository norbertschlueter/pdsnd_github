import time
import pandas as pd
import numpy as np
pd.set_option("display.max_columns",200)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_answered = 'no'
    while city_answered == 'no':
        print('Would you like to see the data for Chicago, New York City, or Washington?')
        city = input().lower()

        cities = ['chicago', 'new york city', 'washington']
        if city in  cities:
            city_answered = 'yes'
        else:
            print('Please define the city for the analysis.')
    # Time filter?
    time_filter_answered = 'no'
    time_filter_list = ['month', 'day', 'both', 'none']
    month = 'all'
    day = 'all'

    while time_filter_answered == 'no':
        print('Would you like to filter the data by month, day, both or not all?')
        print('Type "none" for no time filter')
        time_filter = input()
        print('Time filter: ', time_filter)
        if time_filter in time_filter_list:
            time_filter_answered = 'yes'
        else:
            print('Please define the time filter.')

    # get user input for month (all, january, february, ... , june)
    if time_filter == 'month' or time_filter == 'both':
        month_answered = 'no'
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        while month_answered == 'no':
            print('Which month?')
            month = input().lower()
            if month in months:
                month_answered = 'yes'
            else:
                print('Please define the month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if time_filter == 'day' or time_filter == 'both':
        day_answered = 'no'
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while day_answered == 'no':
            print('Which day?')
            day = input().lower()
            if day in days:
                day_answered = 'yes'
            else:
                print('Please define the day.')
    print()
    print('You will get results for this filter:')
    print('City: ', city.title())
    print('Month:', month.title())
    print('Day: ', day.title())
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
    filename = CITY_DATA[city]

    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    # Returns number of month, Jan = 1, ...
    df['month'] = df['Start Time'] .dt.month
    # Returns number of week day, Monday = 0, ...
    df['day_of_week'] = df['Start Time'] .dt.dayofweek
    # df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1

        # filter by month to create the new dataframe
        maske = df['month'] == month
        df = df[maske]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        maske = df['day_of_week'] == day
        df = df[maske]

    print('Please enter "yes" if you want to see the raw data for the chosen time period, otherwise please enter '
          'any other key.')
    raw_data = input().lower()
    start_line = 0
    end_line = 5
    step = 5
    len_df = len(df)
    while raw_data == 'yes':
        show_df = df.iloc[start_line: end_line]
        print(show_df)
        print('Please enter "yes", if you want to see more more raw data.')
        raw_data = input().lower()
        start_line += step
        end_line += step
        if start_line > len_df:
            print('You reached the end of the data file.')
            raw_data = 'no'
        elif end_line > len_df:
            end_line = len_df

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('The most popular month is:', (months[popular_month -1].title()))

    # display the most common day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day is: ', days[popular_day].title())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    start_station = df['Start Station'].value_counts()
    print('The most popular start station is {} with {} counts.'.format(pop_start_station, start_station[0]))

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    end_station = df['End Station'].value_counts()
    print('The most popular end station is {} with {} counts.'.format(pop_end_station,end_station[0]))

    # display most frequent combination of start station and end station trip
    df['Trip'] = 'from "' + df['Start Station'] + '" to "' + df['End Station'] + '"'
    pop_trip = df['Trip'].mode()[0]
    trip = df['Trip'].value_counts()
    print('The most popular trip is {} with {} counts.'.format(pop_trip,trip[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total trip duration is {} seconds.'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The mean trip duration is {} seconds.'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    print('The statistics of user types and their counts:')
    print(df['User Type'].value_counts())

    if city == "washington":
        print('\nUnfortunately the gender and year of birth are not available for Washington.')
    else:
        # Display counts of gender
        print('T\nhe statistic of gender:')
        gender_stat = df['Gender'].value_counts()
        for i in range(len(gender_stat)):
            print(gender_stat.index[i], gender_stat[i])

        # Display earliest, most recent, and most common year of birth
        year_earliest = df['Birth Year'].min()
        print('\nThe earliest year of birth is: ', year_earliest)
        year_recent = df['Birth Year'].max()
        print('The most recent year of birth is: ', year_recent)
        year_common = df['Birth Year'].mode()
        print('The most common year of birth is: ', year_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()

