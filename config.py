# Defines some constants configuration


##########################
#       Simulation       #
##########################
from astropy import time as astrotime
from astropy import units
from datetime import datetime

# Define starting date of the simulation (start today)
SIM_START_DATE = astrotime.Time(datetime.now().strftime('%Y-%m-%d'))

# Steps at which the simulation integrates
# Use a time unit from astropy.units
# u.d is a day
# u.h is an hour
# u.s is a second
# Keep in mind that putting high values will break the simulation since we are integrating using
# this value as the delta of time elapsed between each cycle.
# So the higher the value, the higher the error for every cycle
# But smaller value means slower simulation.
SIM_DT = 1 * units.d

##########################
#     Informationnal     #
##########################
# Enable debugging prints
DEBUG = False

# Enable verbose
VERBOSE = False

# Enable dumping of position, velocity and accelerations to CSV
CSV = False
CSV_OUTPUT = './logs.csv'

SHOW_FPS = True

##########################
#         Display        #
##########################

# MATPLOTLIB SPECIFICS
# those are unused when using panda3d display
# Time between each frame
FRAME_RATE = 0.0001
FIG_SIZE = 20
SIM_SIZE = 10

# PANDA SPECIFICS
# those are unused when using matplotlib display
# Display size in pixels
DISPLAY_WIDTH = 1800
DISPLAY_HEIGHT = 1100

ZOOM_FACTOR_STEP = 2
DEFAULT_ZOOM = 1.0e-7

HIDE_LABEL = False
LABEL_SIZE = 0.13

# Realist or non realist view
# Setting to true will keep proper ratio between radius and distances
# realist view can be hard to grasp due to the immensity of space
REALIST_VIEW = True

# This option will set all radius to STANDADRD_BODY_SIZE for each body, regardless of the realism choice
# This works best with REALIST_VIEW = True, because the distances will be respected, and objects visible
STANDARDIZE_BODY_SIZES = True
STANDARD_BODY_SIZE = 0.5

# Option for non-realist view, this is use to give a base size for objects
DEFAULT_BODY_SIZES = 2

# History feature allows to print orbits of objects
HISTORY_ON = True
# History size defines the length of the position history of each object
HISTORY_SIZE = 100
# Skip to one point saved every HISTORY_STEP
HISTORY_STEP = 2


##########################
#         Keymap         #
##########################
# Keys can be re-map to anything
# key definition is the one used by panda3d
# https://docs.panda3d.org/1.10/python/programming/hardware-support/keyboard-support
# except for mouse_x and mouse_y which are built-ins

# Those are the keys that can stay pressed
KEYMAP_REP = {
    'UP': 'r',  # move camera upward
    'DOWN': 'f',  # move camera downward
    'FWD': 'w',  # move camera forward
    'LEFT': 'a',  # move camera left
    'BACKWD': 's',  # move camera backward
    'RIGHT': 'd',  # move camera right
    'YAW': 'mouse_x',  # rotate camera on Yaw axis
    'PITCH': 'mouse_y', # rotate camera on pitch axis
    'ROLL_R': 'e',  # rotate camera right on roll axis
    'ROLL_L': 'q',  # rotate camera left on roll axis
    'MVT_SPEED+': '=',  # increase camera movement speed
    'MVT_SPEED-': '-',  # decrease camera movement speed
}

# Those are the keys whose effect is not repeated
KEYMAP_ONCE = {
    'ZOOM_IN': 'wheel_up',  # Zoom in the simulation
    'ZOOM_OUT': 'wheel_down',  # Zoom out of the simultaion
    'TARGET_PREV': 'arrow_left',  # select previous object, automatically rotate camera to look in object's direction
    'TARGET_NEXT': 'arrow_right',  # select next object, automatically rotate camera to look in object's direction
    'FOCUS_TARGET': 'l',  # focus camera on selected object
    'PAUSE': 'p',  # pause the simulation
    'MOUSE_SWITCH_MODE': 'mouse2',  # Switch between camera and select mode
    'DELETE': 'delete',  # delete selected object from simulation
    'HELP': 'f1',  # Display help message
    'QUIT': 'escape'  # quit the simulator
}

CAM_SPEED = 10
CAM_SPEED_STEP = 10
MIN_CAM_SPEED = 0.2
MAX_CAM_SPEED = 100000000

CAM_ROTATION_SPEED = 50
CAM_ROTATION_SPEED_STEP = 1.5
MIN_CAM_ROTATION_SPEED = 10
MAX_CAM_ROTATION_SPEED = 120

# Between 0 and whatever, but we multiply by that number :D
MOUSE_SENSITIVITY = 5
MOUSE_INVERT_X = False
MOUSE_INVERT_Y = False

# Specify if body rotation should continue while the simulation is paused
BODY_ROTATE_ON_PAUSE = True