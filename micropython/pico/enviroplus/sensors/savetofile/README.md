This code is for equipment combo Pico / Enviro+ / PMS5003, and it 
saves data locally on Pico.

It reads:
- **PM** data (very well),
- **temp in Celsius** (very well),
- **light** (very well),
- **humidity** (very well),
- **noise** (not so well),
- **pressure** (very well),
- **gas** (not sure).

Gas sensor I didn't figure out yet what it reads. It does not read (it seems) when harsh
chemicals are felt in the air. Maybe it is not VOC gas.

Data is saved to `sensors.txt` file on Pico. Samples in [/readings](../../doc/readings) folder. 

To send data wirelessly check out [/sensorcommunity](../sensorcommunity/README.md). 

----

Below in the graph and chart you can see that from a safe level (low/green), smoke fills the room and exceeds safety limits. Then it slowly dissipates and reaches safe level again.

This is what it shows on screen: 

![cigarette smoke](../../doc/cigarette%20smoke.jpeg)

This is the sensor data saved to CSV file (colored): 

![cigarette smoke data](../../doc/quick%20smoke.jpg)



Setup
-----
Read contents of [main.py](main.py) for setup and explanations. 


Current issues
--------------

- *major*: the biggest readings files are 809KB, it is very difficult to add memory to Pico, due to only I2C being available 
- *major*: time is not correct when on battery, time is only correct 
  when plugged into a computer (Mac in my case) - it is very difficult to add high temp-resistant RTC clock to Pico 
- *minor*: Pico restarts (when on battery) few times per day (successfully) 

All of these issues are gone when [sending data wirelessly](../sensorcommunity/README.md). 

TODO
----

- How to add SD card to save more data? 
- How to add time component that works in high outdoor temps? 

All of these TODOs are solved when [sending data wirelessly](../sensorcommunity/README.md). 
