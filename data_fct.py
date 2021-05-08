#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
#
# Data manipulations functions for the vegtrug project. 
# Author: Mathias Roesler
# Last modified: 04/21
# Contact: mathias.roesler@univ-reims.fr

import re
import os.path
import numpy as np
import pandas as pd

from misc_fct import *


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


def order_data(data_list, timestamps, csv_file, save_loc):
    """ Uses the data in data_list to create a DataFrame.

    The DataFrame contains in the first column the timestamps, for
    each sensor the data appears in this order: sensor name, L, T, E, S.
    Arguments:
    data_list -- list of dict, contains the data of each sensor.
    timestamps -- list, contains the timestamps at which the values 
    were taken for one day only.
    csv_file -- str, name of the csv_file, _ordered will be appended 
        before saving it.
    save_loc -- str, location to save the csv file, 
        absolute path or pathname.

    Returns:
    ordered_df -- pd.DataFrame, reordered data from data_list.

    """
    ordered_df= pd.DataFrame()
    nb_sensors = len(data_list)
    nb_values = len(data_list[0]['L'])

    for i in range(nb_sensors):
        sensor_data = data_list[i]
        sensor_nb = sensor_data['number']

        # Add the sensor name and the values to the DataFrame.
        ordered_df['sensor_' + sensor_nb] = [sensor_data['name']] + (
                nb_values * [''])
        ordered_df['L_' + sensor_nb] = [''] + sensor_data['L']
        ordered_df['T_' + sensor_nb] = [''] + sensor_data['T']
        ordered_df['E_' + sensor_nb] = [''] + sensor_data['E']
        ordered_df['S_' + sensor_nb] = [''] + sensor_data['S']
        
    # Duplicate timestamps and insert them into the DataFrame.
    nb_days = nb_values // len(timestamps)
    days = ['']

    for i in range(nb_days):
        days = days + ['Day_' + str(i)] + (len(timestamps) - 1) * ['']

    timestamps = [''] + timestamps * (nb_values // len(timestamps))
    ordered_df.insert(0, 'Timestamps', timestamps)
    ordered_df.insert(0, 'Days', days)

    splited_name = save_loc.split('.')
    
    # Save the data.
    ordered_df.to_csv(os.path.join(save_loc, csv_file + '_ordered.csv'),
            index=None)

    return ordered_df


def read_data(csv_file, save_loc):
    """ Reads the data from the input csv file.

    A dictionnary is created for each sensor that contains five keys:
    the sensor name, L the luminosity, E the conductivity, T the
    temperature, and S the soil humidity.
    Arguments:
    csv_file -- str, path to csv file, absolute path or pathname.
    save_loc -- str, location to save the csv file, 
        absolute path or pathname.

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

        try:
            sensor_nb = re.search(r'\d+', sensor_name).group()

        except:
            # If there is no sensor number in the name.
            sensor_nb = str(i+1)

        sensor_data = {'name': sensor_name, 'number': sensor_nb} 

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

        data_list.append(sensor_data)

    timestamps = df[df.columns[0]][2:26].tolist()

    try:
        path_bits = csv_file.split('/')
        csv_file_name = path_bits[-1]

    except:
        csv_file_name = csv_file

    ordered_df = order_data(data_list, timestamps, csv_file_name, save_loc)

    return data_list
