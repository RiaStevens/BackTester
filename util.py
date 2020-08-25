import datetime
import numpy as np


def get_config_from_console():

    initial_investment = int(input('Enter an initial investment: '))
    done = False
    while not done:
        valid = False
        while not valid:
            try:
                start_date = input(
                    'When would you like to begin the stock simulation? Enter a date in DD-MM-YYYY format: ')
                start_day, start_month, start_year = map(int, start_date.split('-'))
                start_date = datetime.datetime(start_year, start_month, start_day)
                start_date = np.datetime64(start_date)
            except:
                print('Please enter a valid date in the specified format!')
                continue
            valid = True

        valid = False
        while not valid:
            try:
                end_date = input('When would you like to end the simulation? Enter a date in DD-MM-YYYY format: ')
                end_day, end_month, end_year = map(int, end_date.split('-'))
                end_date = datetime.date(end_year, end_month, end_day)
                end_date = np.datetime64(end_date)
            except:
                print('Please enter a valid date in the specified format!')
                continue
            valid = True

        if start_date < end_date:
            done = True

        else:
            print('Make sure your start date comes before your end date!')
        return start_date, end_date, initial_investment
def get_config_from_file(config_file_name):
    config_file = open(config_file_name, "r")


    #reading the file line by line and converting to a useful format
    initial_investment = int(config_file.readline())

    start_date = config_file.readline()
    start_day, start_month, start_year = map(int, start_date.split('-'))
    start_date = datetime.datetime(start_year, start_month, start_day)
    start_date = np.datetime64(start_date)

    end_date = config_file.readline()
    end_day, end_month, end_year = map(int, end_date.split('-'))
    end_date = datetime.date(end_year, end_month, end_day)
    end_date = np.datetime64(end_date)
    return start_date, end_date, initial_investment