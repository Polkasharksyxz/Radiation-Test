# Author: YXZ
# Evaluation Board : STM32F446RE
# Main Board : MCU interposer v1
# Program Description: 1.using gpio expander to turn on load switch and RF switch 2. using current sensor to readout assigned channel

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
from machine import SoftI2C
from machine import Pin
from machine import UART
from pyb import Timer
import time
import os
import struct
import gc

i2c = SoftI2C(scl='B6', sda='B7',freq=100000)
i2c.scan()

def turnoff():
    gpioext_addr=0x20
    i2c.writeto_mem(gpioext_addr, 0x03, b'\x00')#configure ports
    time.sleep(0.1)
    i2c.writeto_mem(gpioext_addr, 0x01, b'\x00')

def readCurrentSensor(cs: int, FSV, res):
    #Current Sensor : INA226
    if cs == 0:    
        cs_addr = 0x4C
    elif cs == 1:
       cs_addr = 0x29
    elif cs == 2:
       cs_addr = 0x18
    else:
        raise ValueError("current sensor address")
    i2c = SoftI2C(scl='B9', sda='B8',freq=100000) #yxz
    time.sleep(0.1)
    #soft reset
    try:
        i2c.readfrom_mem(0x00,0x0D,1)
    except Exception:
        time.sleep(0.01)
        pass
    
    try:
        i2c.readfrom_mem(0x00,0x0E,1)
    except Exception:
        time.sleep(0.01)
        pass
    #print("Mux addr: 0x{:02X}, ch: {}, cs addr: {:02X}".format(mux_addr, ch, cs_addr))
    time.sleep(0.1)
    try:
        c0 = i2c.readfrom_mem(cs_addr,0x0D,1)   # Higher byte
        c1 = i2c.readfrom_mem(cs_addr,0x0E,1)
    except:
        print("EX!")
        c0 = b'\x7F'
        c1 = b'\xFF'
    c = c0 + c1
    cur = struct.unpack(">h", c)[0] >> 4
    FSC = FSV/res
    #print(cur/2047*FSC)
    #print(str(cur/2047*FSC)+"mA")
    i2c = SoftI2C(scl='B8', sda='B9',freq=100000)
    time.sleep(0.1)
    return (cur/2047*FSC)

def power_on(sample:int):
    #GPIO Expander : TCA9534PWR
    gpioext_addr=0x20
    i2c.writeto_mem(gpioext_addr, 0x03, b'\x00')#configure ports
    time.sleep(0.01)
    if sample == 1:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x81')
        c=readCurrentSensor(2,FSV,res)
        time.sleep(0.1)
        return c
    elif sample ==2:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x42')
        c=readCurrentSensor(0,FSV,res)
        time.sleep(0.1)
        return c
    elif sample ==3:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x24')
        c=readCurrentSensor(1,FSV,res)
        time.sleep(0.1)
        return c
    elif sample ==4:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x07')
    else:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x00')
        print("power off")

def unbias(sample:int):
    gpioext_addr=0x20
    i2c.writeto_mem(gpioext_addr, 0x03, b'\x00')#configure ports
    time.sleep(0.01)
    if sample == 1:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x40')
    elif sample ==2:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x80')
    elif sample ==3:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x20')
    else:
        i2c.writeto_mem(gpioext_addr, 0x01, b'\x00')
        print("power off")

#turn on all power
power_on(4)

#turn off all power
power_on(0)

#measure channel 1
res=0.1; FSV = 80
gpioext_addr=0x20
i2c.writeto_mem(gpioext_addr, 0x03, b'\x00')#configure ports
#turn on 1
i2c.writeto_mem(gpioext_addr, 0x01, b'\x81')
time.sleep(0.5)
print(readCurrentSensor(0,FSV,res))
#turn on 2
i2c.writeto_mem(gpioext_addr, 0x01, b'\x42')
time.sleep(0.5)
print(readCurrentSensor(1,FSV,res))
#turn on 3
i2c.writeto_mem(gpioext_addr, 0x01, b'\x24')
time.sleep(0.5)
print(readCurrentSensor(2,FSV,res))
#turn on
i2c.writeto_mem(gpioext_addr, 0x01, b'\x80')

power_on(4)

i2c.scan()
