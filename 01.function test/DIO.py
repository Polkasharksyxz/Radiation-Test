from machine import SoftI2C
from machine import Pin
from machine import UART
from pyb import Timer
import time
import os
import struct
import gc

#DO
CE1 = Pin('D7', Pin.OUT)
CE1.value(1)
#DI
TEST = Pin('D6', Pin.IN)
TEST.value()
