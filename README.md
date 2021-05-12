# Vegtrug data analysis

This program analyzes the data produces by VegTrug sensors.

## General information

The program reads a CSV file that contains the sensor readings. Before being
analyzed, the two first rows must be deleted. All of the sensors must have
the same number of measurement for the program to work, i.e. they must all
have functionned the same number of hours and produced a value in the CSV
file (either a number of a - symbol if no measurement occured). 

The program will first read the data in the provided CSV file and reorganize
it before saving it in a new CSV file. It will then divide the data according
to the different groups that were provided and plot it. The default number of
groups is 2: the control group and one testing group. The graphs are saved
alongside the new CSV file. In order to plot the data with no issues, the 
hypothesis is that none of the sensor values will be negative, therefore
if a value is missing (- symbol instead of a number) it will be replaced 
by -1. 


## Package requirements

* Python 3.8 
* Numpy 1.19.5
* Pandas 1.2.2
* Matplotlib 3.3.4
    
## Usage

usage: main.py [-h] [--c sensor_nb [sensor_nb ...]] [--nb_grps nb_grps]
               file save_loc nb_sensors
               
To print the help message use the command:

    $ python3 main.py --help
    
There are three arguments that must be specified, the path to the CSV file,
the path to the folder to save the graphs and the reordered data, and the 
number of sensors used. If the folder for saving the data does not exist, it
will be created. 

    $ python3 main.py csv_file_path save_folder_path 9 
    
There are two optional arguments, nb_grps which indicates the number of testing
group, if not specified its value is 1. The control group should not be 
included. In the following example there will be one control group and three 
testing groups. 

    $ python3 main.py csv_file_path save_folder_path 9 --nb_grps 3
    
The second optional arguments, --control_grp or --c, allows the user to directly
input the sensor numbers that are associated with the control group. In the 
following example sensors 1, 2, and 3 will be the control group.

    $ python3 main.py csv_file_path save_folder_path 9 --c 1 2 3

