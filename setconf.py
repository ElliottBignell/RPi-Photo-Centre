#!/usr/bin/env python

import ConfigParser

config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section('Pins')
config.set('Pins', 'shutterpin', 17)
config.set('Pins', 'solenoidpin', 4)
config.set('Pins', 'camerapin_part', 27)
config.set('Pins', 'camerapin_full', 28)

config.add_section('Delays')
config.set('Delays', 'sleep_inter1', '0.06')
config.set('Delays', 'sleep_inter2', '0.05')
config.set('Delays', 'sleep_inter3', '0.1')
config.set('Delays', 'sleep_exter1', '0.1')
config.set('Delays', 'sleep_exter2', '0.12')

# Writing our configuration file to 'example.cfg'
with open('drops.cfg', 'wb') as configfile:
    config.write(configfile)
