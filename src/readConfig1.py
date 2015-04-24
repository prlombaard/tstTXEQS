#!/usr/bin/env python
"""
Script reads config file
Author: Rudolph Lombaard
Source: Pyhon docs
"""

import ConfigParser

config_location = '../mysrv/mysrv.conf'
json_location = '../mysrv/mysrv.json'

print "Opening Config Located at %s" % config_location

config = ConfigParser.RawConfigParser()
config.read(config_location)

# getfloat() raises an exception if the value is not a float
# getint() and getboolean() also do this for their respective types
frequency = config.getfloat('mysrv', 'frequency')
port_number = config.getint('mysrv', 'port_number')
stereo_playback = config.getboolean('mysrv', 'stereo_playback')
music_dir = config.get('mysrv', 'music_dir')
PIFM_BIN = config.get('mysrv', 'PIFM_BIN')

print "Frequency\t\t: %0.2f" % frequency
print "Port number\t\t: %d" % port_number
print "Stereo Playback\t: %s" % str(stereo_playback)
print "Music dir\t\t: %s" % music_dir
print "PIFM_BIN\t\t: %s" % PIFM_BIN

# Notice that the next output does not interpolate '%(bar)s' or '%(baz)s'.
# This is because we are using a RawConfigParser().

import json

# Source from http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python
# It correctly decodes unicode objects to ascii

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

#server_users_and_passwords = {'user': 'user', 'admin': 'admin'}
#server_debugmode = "logging off"
#server_txmode_string = ['Fixed Frequency', 'Sweep Frequency', 'Hop Frequency', 'Off']
#server_varheader = ['txmode', 'fixedstart', 'fixedstop', 'hopdelay', 'sweepstart', 'sweepstop']
#server_logging_mode = {'Append Log': 'Logging on', 'Rewrite log': 'Logging on', 'Off': 'Logging'}
#server_vars = {server_varheader[0]: server_txmode_string[0], server_varheader[1]: 88900000, server_varheader[2]: 100000000, server_varheader[3]: 200, server_varheader[4]: 1000000, server_varheader[5]: 1200000}

print "Opening JSON Located at %s" % json_location

# Writing our configuration file to 'mysrv.conf'
with open(json_location, 'r') as jsonfile:
    #config.write(jsonfile)
    #mypackage = json.loads(jsonfile.read())
    mypackage = json.loads(jsonfile.read(), object_hook=_decode_dict)    

print mypackage
print type(mypackage)

server_users_and_passwords = mypackage['server_users_and_passwords'] 
server_debugmode = mypackage['server_debugmode']
server_txmode_string = mypackage['server_txmode_string']
server_varheader = mypackage['server_varheader'] 
server_logging_mode = mypackage['server_logging_mode']
server_vars = mypackage['server_vars']

import chardet
import string

mystring = server_debugmode

print type(mystring.encode('ascii'))

encoding = chardet.detect(mystring)
if encoding['encoding'] == 'ascii':
    print 'string is in ascii'
else:
	print 'string is NOT ascii'