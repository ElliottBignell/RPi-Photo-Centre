#!/usr/bin/env python

import os
from time import sleep
import ConfigParser
import RPi.GPIO as GPIO

def switchcallback(channel):

    print("Callback!")

    GPIO.output(solenoidpin,GPIO.HIGH)
    sleep(sleep_inter1)
    GPIO.output(solenoidpin,GPIO.LOW)
        
    sleep(sleep_exter1)
        
    GPIO.output(solenoidpin,GPIO.HIGH)
    sleep(sleep_inter2)
    GPIO.output(solenoidpin,GPIO.LOW)
        
    sleep(sleep_exter2)
        
    GPIO.output(focuspin,GPIO.HIGH)
    GPIO.output(shutterpin,GPIO.HIGH)
    sleep(sleep_inter3)
    GPIO.output(shutterpin,GPIO.LOW)
    GPIO.output(focuspin,GPIO.LOW)

try:

    config = ConfigParser.RawConfigParser()
    config.read('/home/pi/photos/drops.cfg')
    
    focuspin       = config.getint(  'Pins',   'focuspin');
    shutterpin     = config.getint(  'Pins',   'shutterpin');
    solenoidpin    = config.getint(  'Pins',   'solenoidpin');
    camerapin_part = config.getint(  'Pins',   'camerapin_part');
    camerapin_full = config.getint(  'Pins',   'camerapin_full');
    sleep_inter1   = config.getfloat('Delays', 'sleep_inter1');
    sleep_inter2   = config.getfloat('Delays', 'sleep_inter2');
    sleep_inter3   = config.getfloat('Delays', 'sleep_inter3');
    sleep_exter1   = config.getfloat('Delays', 'sleep_exter1');
    sleep_exter2   = config.getfloat('Delays', 'sleep_exter2');
    
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(camerapin_part, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(camerapin_full, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(focuspin,    GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(shutterpin,  GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(solenoidpin, GPIO.OUT, initial=GPIO.LOW)
    
    GPIO.add_event_detect( camerapin_full, GPIO.RISING, callback=switchcallback, bouncetime=300 )
    
    os.environ['CAMERA'] = '1'
    
    while True:
        if os.environ['CAMERA'] == '1':
    
            os.environ['CAMERA'] = '0'
    
            # callback()
            sleep(1)
    
except KeyboardInterrupt:
    GPIO.cleanup() 
