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


def str_to_int(str_list):
    """Converts list of strings to a list of ints.

    Special characters '-' and '--' are erased from data.
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
            pass

    return int_list


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
    freq = 27 # Repeat frequency, number of hours plus 3 lines. 
    nb_sensors = round(len(df)/freq) 
    data_list = [] # List to contain the data of each sensor.

    for i in range(nb_sensors):
        tmp_df = df[i*freq:(i+1)*freq]

        sensor_name = tmp_df[tmp_df.columns[0]][i*freq]
        sensor_data = {'name': sensor_name}

        # Data lists for each quantity.
        L = list()
        E = list()
        S = list()
        T = list()

        for col in tmp_df.columns:
            if tmp_df[col][1 + i*freq] == 'L':
                L.extend(str_to_int(tmp_df[col][2:26].tolist()))

            elif tmp_df[col][1 + i*freq] == 'E':
                E.extend(str_to_int(tmp_df[col][2:26].tolist()))

            elif tmp_df[col][1 + i*freq] == 'S':
                S.extend(str_to_int(tmp_df[col][2:26].tolist()))

            elif tmp_df[col][1 + i*freq] == 'T':
                T.extend(str_to_int(tmp_df[col][2:26].tolist()))

        # Add sensor values to plant dictionnary.
        sensor_data.update({'L': L})
        sensor_data.update({'E': E})
        sensor_data.update({'S': S})
        sensor_data.update({'T': T})

        data_list.append(sensor_data)

    return data_list
