#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
#
# Miscellaneous functions for the vegtrug project.
# Author: Mathias Roesler
# Last modified: 05/21
# Contact: mathias.roesler@univ-reims.fr

import os
import sys
import argparse


def parse_args():
    """ Parses the arguments for the main program.

    Arguments:

    Returns:
    args -- inputed arguments.

    """
    description = "Analyse a csv file, reorders the data, and plots it."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", type=str, help="Path to the csv file to read.") 
    parser.add_argument("save_loc", type=str, 
            help="Save location for the csv file and different graphs.")
    parser.add_argument("nb_sensors", type=int, help="Number of sensors used.")
    parser.add_argument("--c", "--control_grp", type=str, nargs='+', 
            default=None, metavar='sensor_nb', dest='control_group',
            help="Sensor numbers in the control group.")
    parser.add_argument("--nb_grps", type=int, metavar='nb_grps', default=1,
            help="Number of different testing groups other than the control " \
                    "group (default 1).")

    return parser.parse_args()


def error_handler(msg):
    """ Handles errors.

    Arguments:
    msg -- str, error message to print.

    Returns:

    """
    sys.stderr.write("Error: " + msg + "\n")
    exit(1)


def warning_handler(msg):
    """ Handles warnings.

    Arguments:
    msg -- str, warning message to print.

    Returns:

    """
    sys.stderr.write("Warning: " + msg + "\n")


def file_checks(input_file, extension='csv'):
    """ Performs checks on the inputed file.

    The function verifies that the input is a file that exists and
    that has the correct extenstion.
    Arguments:
    input_file -- str, file to verify.
    extension -- str, expected file extension (default csv).

    Returns:

    """
    if not os.path.exists(input_file):
        error_handler("file {} does not exist.".format(input_file))

    if not os.path.isfile(input_file):
        error_handler("{} is not a file.".format(input_file))

    splited_file = input_file.split('.') 

    if splited_file[-1] != extension:
        error_handler("file extension should be {} but got {}".format(
            extension, splited_file[-1]))


def dir_checks(input_dir):
    """ Performs checks on the inputed directory.

    The function verifies that the inputed directory exists, if it
    does it checks if it is a directory, otherwise it creates it.
    Arguments:
    input_dir -- str, path to the directory.

    Returns:

    """
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)

    if not os.path.isdir(input_dir):
        error_handler("selected save location is not a directory.")


def group_checks(grp_list, nb_sensors):
    """ Performs checks on the different groups.

    The function verifies that the numbers in the last group of 
    the list are unique among the other groups and they are in 
    bounds. If not a warning is raised and the number is removed.
    Arguments:
    grp_list -- list of list of str, each item contains the sensor
        numbers for one group. The first group is the control group.
    nb_sensors -- int, number of sensors used.
    
    Returns:
    grp_list -- list of list of str, each item contains the sensor
        numbers for one group. The first group is the control group.

    """
    test_grp = grp_list[-1] # Group to perform checks on.

    for i in range(len(grp_list)):
        for sensor in test_grp:
            if int(sensor) > nb_sensors:
                warning_handler("sensor number {} is greater than the number " \
                        "of sensors. Removing it from current group.".format(
                            sensor))
                test_grp.remove(sensor)

            elif int(sensor) < 0:
                warning_handler("sensor number {} is negative. Removing it " \
                        "from current group.".format(sensor))
                test_grp.remove(sensor)

            if sensor in grp_list[i] and i != len(grp_list)-1:
                if i == 0:
                    warning_handler("sensor number {} is present in control " \
                            "group. Removing it from current group.".format(
                                sensor))

                else:
                    warning_handler("sensor number {} is present in group " \
                            "{}. Removing it from current group.".format(
                                sensor, i+1))
                
                test_grp.remove(sensor)

    return grp_list


def input_checks():
    """ Verifies that the user input is correct.

    Arguments:

    Returns:
    test_grp -- list of str, list of the sensor numbers in group.

    """
    ok = False

    while not ok: 
        user_input = input("Values must be seperated by a comma (no spaces): ")

        try:
            test_grp = user_input.split(',')
            [int(elem) for elem in test_grp]
            ok = True

        except ValueError:
            print("Invalid input.")

    return test_grp
        

def create_groups(nb_grps, nb_sensors, control_group):
    """ Create the different testing groups. 

    Arguments:
    nb_grps -- int, number of testing groups there are.
    nb_sensors -- int, number of sensors used.
    control_group -- list of str, sensor numbers in the control group.

    Returns:
    grp_list -- list of list of str, each item contains the sensor
        numbers for one group. The first group is the control group.

    """
    grp_list = list()
    test_grp = list()

    if control_group == None:
        print("\nPlease specify the sensor numbers in the control group.")
        control_group = input_checks()

    grp_list.append(control_group)
    grp_list = group_checks(grp_list, nb_sensors)

    if nb_grps == 1:
        for sensor in range(1, nb_sensors+1):
            if str(sensor) not in control_group:
                test_grp.append(str(sensor))

        grp_list.append(test_grp)
        grp_list = group_checks(grp_list, nb_sensors)

    else:
        for i in range(nb_grps):
            print("\nPlease specify the sensor numbers in testing group {}" \
                    ".".format(i+1))
            test_grp = input_checks()

            grp_list.append(test_grp)
            grp_list = group_checks(grp_list, nb_sensors)

    return grp_list
