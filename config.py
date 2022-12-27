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

# Graph display size in inches
FIG_SIZE = 15
