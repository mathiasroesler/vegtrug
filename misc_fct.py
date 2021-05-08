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
    description = "Analyse a csv file, reorders the data and plots it."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", type=str, help="Path to the csv file to read.") 
    parser.add_argument("save_loc", type=str, 
            help="Save location for the csv file and different graphs.")
    parser.add_argument("--c", "--control", type=str, nargs='+',  default=1,
            metavar='control_group', dest='control_group',
            help="Sensor numbers in the control group.")

    return parser.parse_args()


def error_handler(msg):
    """ Handles errors.

    Arguments:
    msg -- str, error message to print.

    Returns:

    """
    sys.stderr.write("Error: " + msg + "\n")
    exit(1)


def file_checks(input_file, extension='csv'):
    """ Performs various checks on the inputed file.

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
