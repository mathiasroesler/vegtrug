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
    grp_list = create_groups(args.nb_grps, args.nb_sensors, args.control_group)
    
    test_group = list() # Contains the sensor number not in the control group.
    data_list = read_data(args.file, args.save_loc, args.nb_sensors)

    # Find the sensors that are not in control group.
    for sensor in data_list:
        if sensor['number'] not in args.control_group:
            test_group.append(sensor['number'])
            
    plot_group_data(data_list, grp_list[0], 'Control group', 
            args.save_loc)

    for i in range(args.nb_grps):
        plot_group_data(data_list, grp_list[i+1], "Testing group {}".format(
            i+1), args.save_loc)


    print("Program terminated without errors.")
