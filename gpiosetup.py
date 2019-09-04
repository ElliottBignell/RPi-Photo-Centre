#!/usr/bin/env python

import wiringpi2 as wiringpi

gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_GPIO)  
shutterpin = 17
solenoidpin = 4

gpio.pinMode(shutterpin,gpio.OUTPUT)  
gpio.pinMode(solenoidpin,gpio.OUTPUT)
wiringpi.pinMode(shutterpin,1)
wiringpi.pinMode(solenoidpin,1)

