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
verbose = False

# Enable dumping of position, velocity and accelerations to CSV
csv = False
csv_output = './logs.csv'


##########################
#         Display        #
##########################

# Time between each frame
FRAME_RATE = 0.0001

# Graph display size in pixels
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800

##########################
#         Keymap         #
##########################
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
    'QUIT': 'escape'
}

CAM_SPEED = 10
CAM_SPEED_STEP = 5
MIN_CAM_SPEED = 5
MAX_CAM_SPEED = 100

CAM_ROTATION_SPEED = 20
CAM_ROTATION_SPEED_STEP = 5
MIN_CAM_ROTATION_SPEED = 5
MAX_CAM_ROTATION_SPEED = 100
