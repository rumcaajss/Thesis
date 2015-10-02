#!/usr/bin/python
#-*- coding: utf-8 -*-

from temp_read import *
from gui2 import PageOne, StartPage, controller
import RPi.GPIO as GPIO
print files
new=PageOne(StartPage, controller)
print new.temp_var
while(True):
    for filename in files:
        temp=read_temp(filename)
        print temp
