# Author: YXZ
# Evaluation Board : STM32F446RE
# pin configuration reference: https://os.mbed.com/platforms/ST-Nucleo-F446RE/
# Notion Note: https://finaoyxz.notion.site/STM32F446RE-338c73a15c9143f099a39f25b719cbc6

from machine import SoftI2C
from machine import Pin
from machine import UART
from pyb import Timer
import time
import os
import struct
import gc

#AIO
from pyb import Pin, DAC, ADC
dac = DAC(Pin('A2'))
dac.write(120) # output between 0 and 255
v_write=3.3*120/255
print("Voltage Readout Value: %f V" %v_write)
adc = ADC(Pin('A1')) #A1
adc_value=adc.read() # read value, 0-4095
v_read=3.3*adc_value/4095
print("Voltage Readout Value: %f V" %v_read)