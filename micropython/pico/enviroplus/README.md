This project intends to setup equipement to read gas data (like spray paints) 
and particulates PM1, PM2.5, PM10 (smoke, dust, mold particles). 

It works great for reading and saving PMS data. 

It also reads temp in Celsius (very well), light, humidity (very well), 
noise (not so well), pressure (very well). 

Gas I didn't figure out yet. It does not read (it seems) when harsh chemicals 
are felt in the air. Maybe it is not VOC gas. 

Currently it saves data to `sensors.txt` file. Samples in [/readings](/readings) folder. 


Setup
-----
Read contents of `main.py` for setup and explanations. 


Current issues
--------------

- *major*: it hangs at random point, screen is frozen, no errors 
  caught if catching exceptions - perhaps because of writing to file 
  on Pico's flash?
- *major*: time is not correct when on battery, time is only correct 
  when plugged into a computer (Mac in my case) 
- *minor*: Pico restarts (when on battery) few times per day 


TODO
----

How to fix hanging? 
How to add SD card to save more data? 
How to add time component that works in high temps? 