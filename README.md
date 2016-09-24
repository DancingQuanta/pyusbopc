# pyusbopc

Log an Alphasense OPC via USB-ISS with [dhhagan's py-opc module](https://github.com/dhhagan/py-opc).
The USB adapter is USB-ISS and requires [pyusbiss](https://github.com/DAncingQuanta/pyusbiss).

When executed the script will run indefinitely and sample the OPC every sampling period.
To stop press CTRL+C.

Usage:

```
usbopc device-name period

usbopc /dev/ttyACM0 10
```
Where period is sample period in seconds.
