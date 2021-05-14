import pandas as pd
import numpy as np
import time

source_data = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_data = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
day_data = ['all', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks users to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike share data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_choice = ''
    while city_choice.lower() not in source_data:
        city_choice = input('\n Please enter the city name for which analysis is needed from the following : \n chicago \n new york city \n washington \n :').lower()

        if city_choice in source_data:
            #We were able to get the name of the city to analyze data.
            city = source_data[city_choice.lower()]
            print('You have opted to analyze the data for the city {}'.format(city_choice).upper())
        else:
            #wrong or unknown city to analyze data so we continue the loop to enter data again.
            print('Attention: You have entered the value as {} \n kindly choose a city from the following : \n chicago \n new york city \n washington \n : \n'.format(city_choice))

    #print('\nNext,you will be prompted 2 times , once to select particular month or all , another time for a particular day or all if no filter is needed')

    #get user input for month (all, january, february, ... , june)
    month_name = ''
    while month_name.lower() not in month_data:
            month_name = input("\n For which month would you like to view data? (E.g. Input Either 'all' to apply no month filter or enter a month from January to June months)\n")
            if month_name.lower() in month_data:
                #We were able to get the name of the month to analyze data.
                month = month_name.lower()
            else:
                #wrong month and so we continue the loop.
                print("Attention: You have entered the value as {} and is not a valid input, Please input either 'all' to apply no month filter or enter a month from January to June months\n".format(month_name))

    #get user input for day of week (all, monday, tuesday, ... sunday)
    day_name = ''
    while day_name.lower() not in day_data:
        day_name = input("\n  For which day would you like to view data? (E.g. Input either 'all' to apply no day filter or enter monday,tuesday,wednesday, ... sunday)\n")
        if day_name.lower() in day_data:
            #correct name of the month to analyze data.
            day = day_name.lower()
        else:
            #wrong day and so we continue the loop.
            print("Attention: You have entered the value as {} and is not a valid input, Please input either 'all' to apply no month filter or enter monday, tuesday, wednesday ... , sunday.\n".format(day_name))

    print('-'*40)
    print('You have selected city as {} and to analyze {} month(or months) and to analyse {} day(or days) related cycle trip'.format(city_choice,month,day).upper())
    print('-' * 40)
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
    # load data file based on city selection
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() #NG
    # print(df['day_of_week'])
    df['hour'] = df['Start Time'].dt.hour


    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = month_data.index(month)
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month from the given filtered data is: " + month_data[common_month].title())

    #display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of week from the given filtered data is: " + common_day_of_week)

    #display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print("The most common start hour from the given filtered data is: " + str(common_start_hour) + '\'o clock')

    print("\nThese 3 calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station from the given data is: " + common_start_station)

    #display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station from the given data is: " + common_end_station)

    #display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] + "|" + df['End Station']).mode()[0]
    freq1 = frequent_combination.split("|")
    print("The most popular cycle trip is from -> " + freq1[0] + ' to ->' + freq1[1] )

    print("\nThese 3 calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time from the given data is as" + str(total_travel_time) + ' seconds.')

    #display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time from the given data is as" + str(mean_travel_time) + ' seconds.')

    print("\nThese 2 calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The count of user types from the given data is: \n" + str(user_types))

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()
        print("\nThe count of user gender from the given filtered data is: \n" + str(gender))

        #Display earliest, most recent, and most common year of birth
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print('\nEarliest birth from the given filtered data is: {}\n'.format(earliest_birth))
        print('Most recent birth from the given filtered data is: {}\n'.format(most_recent_birth))
        print('Most common birth from the given filtered data is: {}\n'.format(most_common_birth) )
    else :
        print('\n User Stats like gender,earliest,recent,common births cannot be computed as city selection is neither chicago or NYC')

    print("\nThis user status took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    pd.set_option('display.max_columns', None)
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while True:
            view_raw_data = input('\nWould you like to view first five row of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart i.e. from selecting city list? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()