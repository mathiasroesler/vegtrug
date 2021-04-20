#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
#
# Miscellaneous functions for the vegtrug project.
# Author: Mathias Roesler
# Last modified: 04/21
# Contact: mathias.roesler@univ-reims.fr

import sys
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def parse_args():
    """ Parses the arguments for the main program.

    Arguments:
    Returns:
    args -- inputed arguments.

    """
    description = "Analyse a csv file and plot the data."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", type=str, help="Path to the csv file to read.") 

    return parser.parse_args()


def error_handler(msg):
    """ Handles errors.

    Arguments:
    msg -- str, error message to print.
    Returns:

    """
    sys.stderr.write("Error: " + msg + "\n")
    exit(1)


def file_checks(inputed_file, extension='csv'):
    """ Performs various checks on the inputed file.

    The function verifies that the input is a file that exists and
    that has the correct extenstion.
    Arguments:
    inputed_file -- str, file to verify.
    extension -- str, expected file extension (default csv).
    Returns:

    """
    if not os.path.exists(inputed_file):
        error_handler("file {} does not exist.".format(inputed_file))

    if not os.path.isfile(inputed_file):
        error_handler("{} is not a file.".format(inputed_file))

    splited_file = inputed_file.split('.') 

    if splited_file[-1] != extension:
        error_handler("file extension should be {} but got {}".format(
            extension, splited_file[-1]))


def user_input(filename):
    """ Queries the user to replace file or not if it exists.

    Arguments:
    filename -- str, path to the file.
    Returns:

    """
    if os.exists(filename):
        answer = input("The file {} already exists, do you want to replace it?"\
                " (y/n)".format(filename))
        


def str_to_int(str_list):
    """Converts list of strings to a list of ints.

    Assumption: all of the values are greater than 0.
    When a value is '-' it is replaced by -1. 
    Arguments:
    str_list -- list[str], list of strings.
    Returns: 
    int_list -- list[int], converted list.

    """
    int_list = []

    for elem in str_list:
        try:
            int_list.append(int(elem))

        except ValueError:
            # If the value cannot be converted do nothing.
            int_list.append(-1)

    return int_list


def order_data(data_list, timestamps):
    """ Uses the data in data_list to create a DataFrame.

    The DataFrame contains in the first column the timestamps, for
    each sensor the data appears in this order: sensor name, L, T, E, S.
    Arguments:
    data_list -- list of dict, contains the data of each sensor.
    timestamps -- list, contains the timestamps at which the values 
    were taken for one day only.
    Returns:
    ordered_df -- pd.DataFrame, reordered data from data_list.

    """
    ordered_df= pd.DataFrame()
    nb_sensors = len(data_list)
    nb_values = len(data_list[0]['L'])

    for i in range(nb_sensors):
        sensor_data = data_list[i]
        sensor_nb = sensor_data['name'].split('(')[0] # Get sensor's number.

        # Add the sensor name and the values to the DataFrame.
        ordered_df['sensor_' + sensor_nb] = [sensor_data['name']] + (
                nb_values * [''])
        ordered_df['L_' + sensor_nb] = [''] + sensor_data['L']
        ordered_df['T_' + sensor_nb] = [''] + sensor_data['T']
        ordered_df['E_' + sensor_nb] = [''] + sensor_data['E']
        ordered_df['S_' + sensor_nb] = [''] + sensor_data['S']
        
    # Duplicate timestamps and insert them into the DataFrame.
    nb_days = nb_values // len(timestamps) - 1 
    days = ['']

    for i in range(nb_days):
        days = days + ['Day_' + str(i)] + (len(timestamps) - 1) * ['']


    timestamps = [''] + timestamps * (nb_values // len(timestamps))
    ordered_df.insert(0, 'timestamps', timestamps)
    ordered_df.insert(0, 'days', days)
    ordered_df.to_csv('test.csv')
    breakpoint()

def read_data(csv_file):
    """ Reads the data from the input csv file.

    A dictionnary is created for each sensor that contains five keys:
    the sensor name, L the luminosity, E the conductivity, T the
    temperature, and S the soil humidity.
    Arguments:
    csv_file -- str, path to csv file.
    Returns:
    data_list -- list of dict, contains the data of each sensor.
    """
    df = pd.read_csv(csv_file)
    ordered_df = pd.DataFrame()
    freq = 27 # Repeat frequency, 24 hours plus 3 lines. 
    nb_sensors = round(len(df)/freq) 
    data_list = [] # List to contain the data of each sensor.

    for i in range(nb_sensors):
        tmp_df = df[i*freq:(i+1)*freq]

        sensor_name = tmp_df[tmp_df.columns[0]][i*freq]
        sensor_nb = sensor_name.split('(')[0]
        sensor_data = {'name': sensor_name} 

        # Data lists for each quantity.
        L = list()
        E = list()
        S = list()
        T = list()

        for col in tmp_df.columns:
            if tmp_df[col][1 + i*freq] == 'L':
                L.extend(tmp_df[col][2:26].tolist())

            elif tmp_df[col][1 + i*freq] == 'E':
                E.extend(tmp_df[col][2:26].tolist())

            elif tmp_df[col][1 + i*freq] == 'S':
                S.extend(tmp_df[col][2:26].tolist())

            elif tmp_df[col][1 + i*freq] == 'T':
                T.extend(tmp_df[col][2:26].tolist())

        # Add sensor values to plant dictionnary.
        sensor_data.update({'L': str_to_int(L)})
        sensor_data.update({'E': str_to_int(E)})
        sensor_data.update({'S': str_to_int(S)})
        sensor_data.update({'T': str_to_int(T)})

        ordered_df['sensor_' + sensor_nb] = [sensor_name] + (len(L)-1) * ['-']
        ordered_df['L_' + sensor_nb] = L
        ordered_df['T_' + sensor_nb] = T
        ordered_df['E_' + sensor_nb] = E
        ordered_df['S_' + sensor_nb] = S

        data_list.append(sensor_data)

    # Add an extra lign above everything with the names and remove name from therest
    timestamps = df[df.columns[0]][2:26].tolist()
    ordered_df = order_data(data_list, timestamps)

    # Save reordered data.

    breakpoint()
    return data_list
