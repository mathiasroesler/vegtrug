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
