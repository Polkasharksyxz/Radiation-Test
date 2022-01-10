# Author: YXZ
# Evaluation Board : STM32F446RE
# Current Sensor tested : INA219
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

i2c = SoftI2C(scl='B8', sda='B9',freq=100000)#assign the i2c pin config
data = i2c.readfrom_mem(0x47,0x01,2)
R = 0.1
rdata_I = struct.unpack("h",struct.pack("<BB", data[0], data[1]))
print(data)
