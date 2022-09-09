import configparser

"""
Module parses config file and provides config dict to other modules
"""

config = configparser.ConfigParser()
config.read('config.ini')
