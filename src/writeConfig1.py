#!/usr/bin/env python
"""
Script creates initial config files read by mysrv.py
Author: Rudolph Lombaard
Source: Python docs
"""

import ConfigParser

config_location = '../mysrv/mysrv.conf'
json_location = '../mysrv/mysrv.json'


config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section('mysrv')
config.set('mysrv', 'port_number', '80')
config.set('mysrv', 'stereo_playback', 'true')
config.set('mysrv', 'frequency', '88.9')
config.set('mysrv', 'music_dir', '/boot/music')
config.set('mysrv', 'PIFM_BIN', '/home/pi/pirateradio/pifm')

print "Writing to Config File Located at %s" % config_location

# Writing our configuration file to 'mysrv.conf'
with open(config_location, 'wb') as configfile:
    config.write(configfile)

import json

# TODO: #1, Load securely from config file
server_users_and_passwords = {'user': 'user', 'admin': 'admin'}
server_debugmode = "logging off"
server_txmode_string = ['Fixed Frequency', 'Sweep Frequency', 'Hop Frequency', 'Off']
server_varheader = ['txmode', 'fixedstart', 'fixedstop', 'hopdelay', 'sweepstart', 'sweepstop']
server_logging_mode = {'Append Log': 'Logging on', 'Rewrite log': 'Logging on', 'Off': 'Logging'}
server_vars = {server_varheader[0]: server_txmode_string[0], server_varheader[1]: 88900000, server_varheader[2]: 100000000, server_varheader[3]: 200, server_varheader[4]: 1000000, server_varheader[5]: 1200000}

mypackage = {}
mypackage['server_users_and_passwords'] = server_users_and_passwords
mypackage['server_debugmode'] = server_debugmode
mypackage['server_txmode_string'] = server_txmode_string
mypackage['server_varheader'] = server_varheader
mypackage['server_logging_mode'] = server_logging_mode
mypackage['server_vars'] = server_vars

print mypackage


# Writing our configuration file to 'mysrv.conf'
with open(json_location, 'w') as jsonfile:
    #config.write(jsonfile)
    json.dump(mypackage, jsonfile)
