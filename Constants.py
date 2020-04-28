import os
import sys
import configparser

# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

CONFIG_FILE = os.path.dirname(__file__) + '/config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
config.sections()

APPLICATION_STYLE = config['window_style']['application_style']

# three getter method: getint, getboolean, getfloat
# logViewer = config['main_default']['show_log_viewer']                     # return String
SHOW_LOG_VIEWER = config['log'].getboolean('show_log_viewer')      # return Boolean

# TreeWidget, TreeView Columns
TREE_COL_0 = 0
TREE_COL_1 = 1
TREE_COL_2 = 2
TREE_COL_3 = 3
