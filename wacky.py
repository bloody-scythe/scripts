#!/usr/bin/python3
from sys import argv
from os import system
from subprocess import Popen, PIPE, STDOUT

#----- Functions -----#
def get_curr_area(id):
    id = str(id)
    """Gets a tablet's current area with xsetwacom."""
    process = Popen(['xsetwacom', '--get', id, 'area' ], stdout=PIPE, stderr=STDOUT)
    area = process.stdout.read().decode().split()

    return area

def get_default_area(id):
    id = str(id)
    """Gets a tablet's default area with xsetwacom."""
    #Save current area to not lose it
    curr_area = get_curr_area(id)

    #Reset area to default value for measure
    set_prop(id, "ResetArea")
    process = Popen(['xsetwacom', '--get', id, 'area' ], stdout=PIPE, stderr=STDOUT)
    default_area = process.stdout.read().decode().split()

    #Restore original area back
    set_prop(id, "area", ' '.join(curr_area))

    return default_area

def get_curr_mode(id):
    id = str(id)
    """Gets a tablet's current mode with xsetwacom."""
    process = Popen(['xsetwacom', '--get', id, 'mode' ], stdout=PIPE, stderr=STDOUT)
    mode = process.stdout.read().decode().rstrip()
    return mode

def get_stylus_id():
    """gets the device id of connected stylus"""
    from re import search
    process = Popen(['xsetwacom', '--list' ], stdout=PIPE, stderr=STDOUT)
    ids = process.stdout.read().rstrip().decode()
    stylus_id=search('\tid: ..\ttype: STYLUS', ids).group().split()

    return stylus_id[1]

def toggle_mode(id):
    id = str(id)
    mode = get_curr_mode(id)
    if mode == "Absolute":
        set_prop(id, "mode", "Relative")
    elif mode == "Relative":
        set_prop(id, "mode", "Absolute")


def set_prop(id,*command):
    id = str(id)
    system('xsetwacom --set ' + id + ' ' + ' '.join(command))


#----- MAIN -----#

help = "This is the help text. It's not ready.\n Options are:\n\t--mode_toggle(-mt)\n\t--small(-s)\n\t--full(-f)\n\t--help(-h)"


if __name__ == "__main__":
    id = get_stylus_id()

    if "--mode_toggle" in argv or '-mt' in argv: toggle_mode(id)

    if "--small" in argv or '-s' in argv:
        set_prop(id, "area", "5000 5700 10200 8550")
    elif "--full" in argv or '-f' in argv:
        set_prop(id, "area", "0 0 15200 8550")

    if '--help' in argv or '-h' in argv: print(help)

