#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
#
# Main program.
# Author: Mathias Roesler
# Last modified: 04/21
# Contact: mathias.roesler@univ-reims.fr

from misc_fct import *
from data_fct import *


if __name__ == '__main__':
    args = parse_args()
    
    file_checks(args.file)

    data_list = read_data(args.file)

    print("Program terminated without errors.")
