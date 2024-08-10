In order to register a device in [sensor.community](https://sensor.community/en/) one needs a serial number. 

This code is displaying Pico's serial number. 

But you don't really need it! It is enough to run a simple [hello world](../hello/source.c) in VS code > **Run** in bottom right corner: you will see the serial number displayed in VS Code Terminal when it flashes it onto Pico.

![pico flashing in VS Code](doc/serial%20number%20in%20VS%20Code%20when%20flashing.png)

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

This must be my hub, that does not work well with Pico, for some reason. 

After changing the USB connection I was able to run the code on Pico, as seen in Thonny: 

![code running in Pico](doc/serial%20number%20code%20running%20on%20Pico%20as%20seen%20in%20Thonny.png)
