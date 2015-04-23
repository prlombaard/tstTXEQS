#!/usr/bin/env python

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('mysrv.conf')

# getfloat() raises an exception if the value is not a float
# getint() and getboolean() also do this for their respective types
a_float = config.getfloat('mysrv', 'frequency')
an_int = config.getint('mysrv', 'port_number')
print a_float + an_int

# Notice that the next output does not interpolate '%(bar)s' or '%(baz)s'.
# This is because we are using a RawConfigParser().
if config.getboolean('mysrv', 'stereo_playback'):
    print config.get('mysrv', 'music_dir')
