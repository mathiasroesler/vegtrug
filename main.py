#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
#
# Main program.
# Author: Mathias Roesler
# Last modified: 05/21
# Contact: mathias.roesler@univ-reims.fr

from misc_fct import *
from data_fct import *
from plot_fct import *


if __name__ == '__main__':
    args = parse_args()
    
    file_checks(args.file)
    dir_checks(args.save_loc)

    test_group = list() # Contains the sensor number not in the control group.
    data_list = read_data(args.file, args.save_loc)

    # Find the sensors that are not in control group.
    for sensor in data_list:
        if sensor['number'] not in args.control_group:
            test_group.append(sensor['number'])
            
    plot_group_data(data_list, args.control_group, 'Control group', 
            args.save_loc)
    plot_group_data(data_list, test_group, 'Test group', 
            args.save_loc)


    print("Program terminated without errors.")
