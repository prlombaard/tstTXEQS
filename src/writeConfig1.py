#!/usr/bin/env python

print "hello world"

import ConfigParser

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

# Writing our configuration file to 'mysrv.conf'
with open('mysrv.conf', 'wb') as configfile:
    config.write(configfile)
