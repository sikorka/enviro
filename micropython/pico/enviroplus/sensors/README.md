This code is for equipment combo: Pico / Enviro+ / PMS5003. 

It works great for reading and saving locally **PM** data. It also reads **temp in Celsius** (very well), **light**, **humidity** (very well), **noise** (not so well), **pressure** (very well). 

Gas I didn't figure out yet. It does not read (it seems) when harsh 
chemicals are felt in the air. Maybe it is not VOC gas. 

It saves data to `sensors.txt` file. Samples in [/readings](../doc/readings) folder. 

To send data wirelessly check out [/sensorcommunity](../sensorcommunity/README.md). 

----

Below in the graph and chart you can see that from a safe level (low/green), smoke fills the room and exceeds safety limits. Then it slowly dissipates and reaches safe level again.

This is what it shows on screen: 

![cigarette smoke](../doc/cigarette%20smoke.jpeg)

This is the sensor data saved to CSV file (colored): 

![cigarette smoke data](../doc/quick%20smoke.jpg)



Setup
-----
Read contents of [main.py](main.py) for setup and explanations. 


Current issues
--------------

- *major*: the biggest readings files are 809KB, it is very difficult to add memory to Pico, due to only I2C being available 
- *major*: time is not correct when on battery, time is only correct 
  when plugged into a computer (Mac in my case) - it is very difficult to add high temp-resistant RTC clock to Pico 
- *minor*: Pico restarts (when on battery) few times per day (successfully) 


TODO
----

- How to add SD card to save more data? 
- How to add time component that works in high outdoor temps? 
