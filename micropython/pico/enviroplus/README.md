This code is for equipment combo: Pico / Enviro+ / PMS5003. 

It works great for reading and saving **PM** data. It also reads **temp 
in Celsius** (very well), **light**, **humidity** (very well), **noise** 
(not so well), **pressure** (very well). 

Gas I didn't figure out yet. It does not read (it seems) when harsh 
chemicals are felt in the air. Maybe it is not VOC gas. 

Currently, it saves data to `sensors.txt` file. Samples in 
[/readings](./readings) folder. 

This is what it shows on screen: 
![cigarette smoke](./doc/cigarette%20smoke.jpeg)

Setup
-----
Read contents of [main.py](./main.py) for setup and explanations. 


Current issues
--------------

- *major*: it hangs at random point, screen is frozen, no errors 
  caught if catching exceptions - perhaps because of writing to file 
  on Pico's flash? the biggest readings files are 809KB 
- *major*: time is not correct when on battery, time is only correct 
  when plugged into a computer (Mac in my case) 
- *minor*: Pico restarts (when on battery) few times per day (successfully)


TODO
----

- How to fix hanging? 
- How to add SD card to save more data? 
- How to add time component that works in high outdoor temps? 