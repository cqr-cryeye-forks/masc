"""
Some contants to use
"""
import os
import pathlib

# This is the local directory where I make some test with fake websites
TEST_DIR = "test/"

# Differents local path to make some tests
WORDPRESS_DIR = TEST_DIR + "wordpress/"
JOOMLA_DIR = TEST_DIR + "joomla/"
DRUPAL_DIR = TEST_DIR + "druptal/"
MAGENTO_DIR = TEST_DIR + "magento/"

# The dir where clean installations are downloaded and unzipped
CACHE_DIR = "cache/"

# The dir where backups are stored
BACKUPS_DIR = "backups/"

# Logs dir
LOGS_DIR = "logs/"

ROOT_PATH = pathlib.Path(__file__).parent.absolute()

# The dir to get_links and load_links
OUTPUT_FILE = ROOT_PATH.joinpath("output.txt")
PATH_TO_CONTENT_FOLDER = ROOT_PATH.joinpath("check_result")
if not os.path.exists(PATH_TO_CONTENT_FOLDER):
    os.makedirs(PATH_TO_CONTENT_FOLDER)

# The dict to output data
result_dict = {}
