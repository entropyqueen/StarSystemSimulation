# Defines some constants configuration


##########################
#       Simulation       #
##########################
from astropy import time as astrotime
from astropy import units
from datetime import datetime

# Define starting date of the simulation (start today)
SIM_START_DATE = astrotime.Time(datetime.now().strftime('%Y-%m-%d'))

# Numbers of days to run the simulation for
MAX_DAYS = 100000

# Steps at which the simulation integrates
# Use a time unit from astropy.units
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


##########################
#         Display        #
##########################

# Time between each frame
FRAME_RATE = 0.0001
FIG_SIZE = 20

# Graph display size in pixels
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800

##########################
#         Keymap         #
##########################
# Keys can be re-map to anything
# key definition is the one used by panda3d
# https://docs.panda3d.org/1.10/python/programming/hardware-support/keyboard-support
# except for mouse_x and mouse_y which are built-ins
KEYMAP = {
    'UP': 'r',
    'DOWN': 'f',
    'FWD': 'w',
    'LEFT': 'a',
    'BACKWD': 's',
    'RIGHT': 'd',
    'YAW': 'mouse_x',
    'PITCH': 'mouse_y',
    'ROLL_R': 'e',
    'ROLL_L': 'q',
    'ZOOM_IN': 'wheel_up',
    'ZOOM_OUT': 'wheel_down',
    'MVT_SPEED+': '=',
    'MVT_SPEED-': '-',
    'TARGET_PREV': 'arrow_left',
    'TARGET_NEXT': 'arrow_right',
    'QUIT': 'escape'
}

CAM_SPEED = 10
CAM_SPEED_STEP = 5
MIN_CAM_SPEED = 5
MAX_CAM_SPEED = 100

CAM_ROTATION_SPEED = 50
CAM_ROTATION_SPEED_STEP = 10
MIN_CAM_ROTATION_SPEED = 10
MAX_CAM_ROTATION_SPEED = 120

# Between 0 and whatever, but we multiply by that number :D
MOUSE_SENSITIVITY = 5
MOUSE_INVERT_X = False
MOUSE_INVERT_Y = False
