In order to register a device in [sensor.community](https://sensor.community/en/) one needs a serial number. 

This code is supposed to display Pico's serial number. 

After  successfully flashing onto Pico, unfortunately it displays error: 

```
Unable to connect to /dev/cu.usbmodem1412201: [Errno 2] could not open port /dev/cu.usbmodem1412201: [Errno 2] No such file or directory: '/dev/cu.usbmodem1412201'

Process ended with exit code 1.
```

This command gives me:

    $ sudo ls -la /dev/cu.*
    crw-rw-rw-  1 root  wheel  0x16000001  2 Aug 15:45 /dev/cu.BLTH

