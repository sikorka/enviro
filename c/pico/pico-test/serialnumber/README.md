In order to register a device in [sensor.community](https://sensor.community/en/) one needs a serial number. 

This code is displaying Pico's serial number. 

First things first
------------------

In order to start coding in C on Raspberry Pi Pico, you need to setup VS Code. Go through this amazing tutorial in order to do that https://blog.smittytone.net/2021/02/02/program-raspberry-pi-pico-c-mac/. 

For using various C libraries for Pico, use this reference guide https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf for library names and APIs. 

Once VS Code is setup
---------------------

To read Pico serial number, it is enough to run a simple [hello world](../hello/source.c) in VS code > **Run** in bottom right corner: you will see the serial number displayed in VS Code Terminal when it flashes it onto Pico. 

![pico flashing in VS Code](doc/serial%20number%20in%20VS%20Code%20when%20flashing.png)

Run
---

Clone this repo > open folder [serialnumber](./) in VS Code > in bottom right corner press **Run**. 

Open Thonny > remove and insert Pico once again into your computer's USB > observe the log in Thonny. 

You can also connect to Pico (to see the log) using screen emulator (`screen` or `minicom` on Mac). 

    $ sudo ls -la /dev/cu.*
    Password:
    crw-rw-rw-  1 root  wheel  0x16000001 10 Aug 12:42 /dev/cu.BLTH
    crw-rw-rw-  1 root  wheel  0x16000003 10 Aug 12:54 /dev/cu.usbmodem14301

    screen /dev/cu.usbmodem14301
    
    minicom -D /dev/cu.usbmodem14301

USB problems
------------

If it does NOT show the serial number - as it should - try changing your USB hub. 

Also run: 
    
    $ sudo ls -la /dev/cu.*
    Password:
    crw-rw-rw-  1 root  wheel  0x16000001 10 Aug 12:42 /dev/cu.BLTH
    crw-rw-rw-  1 root  wheel  0x16000003 10 Aug 12:54 /dev/cu.usbmodem14301

Before I connected the second USB, that works better with Pico, I was getting only:

    $ sudo ls -la /dev/cu.*
    crw-rw-rw-  1 root  wheel  0x16000001  2 Aug 15:45 /dev/cu.BLTH


After changing the USB connection I was able to run the code on Pico, as seen in Thonny: 

![code running in Pico](doc/serial%20number%20code%20running%20on%20Pico%20as%20seen%20in%20Thonny.png)
