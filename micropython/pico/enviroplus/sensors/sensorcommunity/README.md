This code is for equipment combo Pico W / Enviro+ / PMS5003, and it sends data 
to https://sensor.community.

It works great for reading **PM** data. It also reads **temp in Celsius** (very well), 
**light**, **humidity** (very well), **noise** (not so well), **pressure** (very well).

Gas I didn't figure out yet. It does not read (it seems) when harsh
chemicals are felt in the air. Maybe it is not VOC gas.

To save data locally, without wifi, read [sensors data saving](../sensorsave/README.md).

----

Below in the graph and chart you can see, that from a safe level (low/green), 
smoke fills the room and exceeds safety limits. Then it slowly dissipates and 
reaches safe level again.

This is what it shows on screen:

![cigarette smoke](../../doc/cigarette%20smoke.jpeg)


Setup
-----
Read contents of [main.py](main.py) for setup and explanations.



