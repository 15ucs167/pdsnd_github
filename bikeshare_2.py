import time
import pandas as pd
import numpy as np

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

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    print('\n\n')
    print('Hello! Let\'s explore some US bikeshare data!\n\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('Which City do you Want to Explore?\n\n')
        user_city = input('chicago, new york city or washington?\n\n')
        city = user_city.lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        else:
            print('Invalid Input. Make sure you type city with the exact spacing and spelling.\n\n')

    #Calling function to print raw data on user request after obtaining city.
    print_raw_data(city)

    # get user input for month (all, january, february, ... , june)
    while(True):
        print('For which month do you want to see the data?\n\n')
        month = input('all, january, february, march, april, may, june ?\n\n').lower()
        if month in months:
            break
        else:
            print('Please enter a valid month from the given options. Make sure you\'ve got the spelling right.\n\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        print('Which day of the given month do you want to explore?\n\n')
        day = input('all, monday, tuesday, wednesday, thursday, friday, saturday, sunday?\n\n').lower()
        if day in days:
            break
        else:
            print('Invalid Input. Please choose from the given options and make sure the spelling\'s right.\n\n')

    print('-'*40)
    return city, month, day

def print_raw_data(city):
    #According to the city chosen by the user, the data of the corresponding csv file is displayed five lines at a time
    while True:
        print('Would you like to read the first five lines of the data file?\n\n')
        answer = input('Enter yes or no\n\n')
        if answer.lower() == 'yes':
            with open(CITY_DATA[city], 'r') as f:
                for i in range(5):
                    print(f.readline())
                while True:
                    print('Would you like to read the next five lines of the file?\n\n')
                    response = input('Enter yes or no\n\n')
                    if response == 'no':
                        break
                    elif response == 'yes':
                        for i in range(5):
                            print(f.readline())
                    else:
                        print('Invalid Input. Please enter yes or no\n\n')
            break

        elif answer.lower() == 'no':
            break

        else:
            print('Please Enter a Valid Response\n\n')

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
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week']== day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()
    print('The most common month(s):', common_month.values)
    print('Where:')
    print('1 => January')
    print('2 => February')
    print('3 => March')
    print('4 => April')
    print('5 => May')
    print('6 => June')
    print('\n\n')


    # display the most common day of week
    common_day = df['day_of_week'].mode()
    print('The most common day(s) of the week:', common_day.values)
    print('Where:')
    print('0 => Monday')
    print('1 => Tuesday')
    print('2 => Wednesday')
    print('3 => Thursday')
    print('4 => Friday')
    print('5 => Saturday')
    print('6 => Sunday')
    print('\n\n')

    # display the most common start hour
    df['Start Hour']= df['Start Time'].dt.hour
    print('The most common start hour(s):')
    common_hour = df['Start Hour'].mode()
    print(common_hour.values)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()
    print('Most Commonly Used Start Station(s): ', common_start.values)
    print('\n\n')

    # display most commonly used end station
    common_end = df['End Station'].mode()
    print('Most Commonly Used End Station(s): ',common_end.values)
    print('\n\n')

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' TO ' + df['End Station']
    common_trip = df['Trip'].mode()
    print('Most Common Trip :', common_trip.values)
    print('\n\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time: {} seconds '.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average Trip Duration: {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of User Types: ')
    print(user_types)
    print('\n\n')
    try:
        # Display counts of gender
        gender_count  = df['Gender'].value_counts()
        print('Counts of Gender: ')
        print(gender_count)
        print('\n\n')

        # Display earliest, most recent, and most common year of birth
        print('Earliest Year of Birth: ', int(df['Birth Year'].min()))
        print('Most Recent Year of Birth: ', int(df['Birth Year'].max()))
        print('Most common year of birth: ', int(df['Birth Year'].mode().values))

    except:
        print('The data about gender and birth year isn\'t available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
