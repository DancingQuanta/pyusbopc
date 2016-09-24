#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Log an Alphasense OPC via USB-ISS dhhagan's py-opc module at
https://github.com/dhhagan/py-opc.

The USB adapter is USB-ISS and requires
https://github.com/DAncingQuanta/pyusbiss

When executed the script will run indefinitely and sample the OPC every
sampling period.
To stop press CTRL+C.

Usage:
    usbopc device-name period

    usbopc /dev/ttyACM0 10

Where period is sample period in seconds.

"""

import os
import sys
from time import sleep, time, strftime, localtime
from datetime import datetime
import usbiss
import opc
import json


# Get arguments
if len(sys.argv) != 3:
    print('Usage: {} device-name period'.format(sys.argv[0]))
    sys.exit(1)

# Port
port = sys.argv[1]

# Sample period
period = int(sys.argv[2])

# Open connection to USB-ISS in SPI mode.
usb = usbiss.USBISS(port, 'spi', spi_mode=2, freq=500000)

# Get infomration about USB-ISS
usb.get_iss_info()

# Give the USB connection to py-opc
alpha = opc.OPCN2(usb)

# Toggle to tur on properly
alpha.off()
sleep(1)

alpha.on()
sleep(1)

alpha.off()
sleep(1)

alpha.on()
sleep(1)

# Get config from OPC and print to file
config = alpha.config()
config2 = alpha.config2()
print(config)
print(config2)

configfile = 'config.json'
with open(configfile, 'w') as handle:
    json.dump(config, handle, sort_keys=True, indent=4)

configfile = 'config2.json'
with open(configfile, 'w') as handle:
    json.dump(config, handle, sort_keys=True, indent=4)

# Create a log file
logfile = strftime("%Y-%m-%d_%H-%M-%S", localtime())
print("Opening Output File: " + logfile)
f = open(logfile, 'w')

# log data
print("Logging. To stop press CTRL+C.")
lastUpdated = 0

try:
    while True:
        curTime = time()
        if (curTime-lastUpdated) >= period:
            lastUpdated = curTime

            # Get histogram
            data = alpha.histogram()

            # tnow = datetime.fromtimestamp(curTime).strftime("%Y-%m-%d %H:%M:%S")
            tnow = datetime.fromtimestamp(curTime)

            line = [tnow,
                    data['Bin 0'], data['Bin 1'], data['Bin 2'],
                    data['Bin 3'], data['Bin 4'], data['Bin 5'],
                    data['Bin 6'], data['Bin 7'], data['Bin 8'],
                    data['Bin 9'], data['Bin 10'], data['Bin 11'],
                    data['Bin 12'], data['Bin 13'], data['Bin 14'],
                    data['Bin 15'], data['Bin1 MToF'], data['Bin3 MToF'],
                    data['Bin5 MToF'], data['Bin7 MToF'],
                    data['Sampling Period'], data['Temperature'],
                    data['Pressure'], data['PM1'], data['PM2.5'],
                    data['PM10']]

            data = ','.join(str(e) for e in line) + '\n'

            # Write to file
            f.write(data)
            f.flush()  # Properly write to disk
            print(data)
except KeyboardInterrupt:
    print("Closing:")
    f.close()
    alpha.off()
    usb.close()
