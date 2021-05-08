#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
#
# Plotting functions for the vegtrug project. 
# Author: Mathias Roesler
# Last modified: 05/21
# Contact: mathias.roesler@univ-reims.fr

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from misc_fct import error_handler


def plot_fct(ax, data, y_label, x_label="Time in hours", grid='both'):
    """ Plots the given data.

    Arguments:
    ax -- subplot to plot the data on.
    data -- list, data to be plotted.
    y_label -- str, label for the y axis.
    x_label -- str, label for the x axis (default Time in hours).
    grid -- str, {'major', 'minor', 'both'} grid lines to show 
    (default both).
    
    Returns:
    figure_handle -- handle for the current subplot.

    """
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True, which=grid)
    
    return ax.plot(np.arange(len(data)), data)


def plot_group_data(data_list, group, figure_title, save_loc):
    """ Plots the data for a given group.

    Arguments:
    data_list -- list of dict, contains the data of each sensor.
    group -- list of int, contains the sensor numbers for the group.
    figure_title -- str, title for the figure.
    save_loc -- str, location to save the figure, absolute path or pathname.

    Returns:

    """
    try:
        assert(os.path.exists(save_loc))
        assert(os.path.isdir(save_loc))

    except AssertionError:
        error_handler("Invalid save location.")

    # Create figure for plotting.
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
    handles = list() # List of handles for the legend.
    legend_labels = list() # List of labels for the legend.

    for sensor in data_list:
        if sensor['number'] in group:
            # If the sensor number is in the group.
            # Plot conductivity.
            handles.append(plot_fct(ax1, sensor['E'], r"EC ($\mu$/cm)")[0])

            # Plot light.
            plot_fct(ax2, sensor['L'], "Light (mmol)") 

            # Plot soil humidity.
            plot_fct(ax3, sensor['S'], "Soil humidity (%)")

            # Plot temperature.
            plot_fct(ax4, sensor['T'], "Temperature (C)")

            legend_labels.append(sensor['number'])

    # Add titles to subplot and figure.
    ax1.title.set_text('Conductivity')
    ax2.title.set_text('Luminosity')
    ax3.title.set_text('Humidity')
    ax4.title.set_text('Temperature')
    fig.suptitle(figure_title)

    fig.legend(handles, legend_labels, loc='center right')

    plt.savefig(os.path.join(save_loc, figure_title)) 
    plt.show()
