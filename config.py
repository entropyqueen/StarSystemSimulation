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

# MATPLOTLIB SPECIFICS
# those are unused when using panda3d display
# Time between each frame
FRAME_RATE = 0.0001
FIG_SIZE = 20

# PANDA SPECIFICS
# those are unused when using matplotlib display
# Display size in pixels
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800

ZOOM_FACTOR_STEP = 2
DEFAULT_ZOOM = 1

DEFAULT_BODY_SIZES = 2

##########################
#         Keymap         #
##########################
# Keys can be re-map to anything
# key definition is the one used by panda3d
# https://docs.panda3d.org/1.10/python/programming/hardware-support/keyboard-support
# except for mouse_x and mouse_y which are built-ins

# Those are the keys that can stay pressed
KEYMAP_REP = {
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
    'MVT_SPEED+': '=',
    'MVT_SPEED-': '-',
}

# Those are the keys whose effect is not repeated
KEYMAP_ONCE = {
    'ZOOM_IN': 'wheel_up',
    'ZOOM_OUT': 'wheel_down',
    'TARGET_PREV': 'arrow_left',
    'TARGET_NEXT': 'arrow_right',
    'FOCUS_TARGET': 'l',
    'PAUSE': 'p',
    'QUIT': 'escape'
}

CAM_SPEED = 10
CAM_SPEED_STEP = 1.5
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
