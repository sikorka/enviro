import network
import secrets
import socket
import time
import machine

from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from pimoroni import RGBLED, Button
from pimoroni_i2c import PimoroniI2C

"""
This demoes a small web server for Pico/Enviro+ combo. 

It serves a small web page on Pico, that enables turning Enviro+ led on and off. 
It also shows reading of temperature from BME sensor. 

Both devices, Pico and device with browser, need to be on same WIFI. 

SETUP:
1. copy this file to your Pico
2. in file `secrets.py` on your Pico, input:
   SSID = "WIFI NAME"
   PASSWORD = "WIFI PASS"
3. connect Pico to your computer and run this file (e.g. in Thonny)
4. open in browser the IP address that is printed on screen
5. play with the LED ON and LED OFF buttons

If you want to exit the program in a nice way, hold the X button, while
refreshing the page in browser.

"""


# set up the buttons
button_a = Button(12, invert=True)
button_b = Button(13, invert=True)
button_x = Button(14, invert=True)
button_y = Button(15, invert=True)

# wifi connection
wlan = 0
connection = 0
client = 0

# set up the LED
led = RGBLED(6, 7, 10, invert=True)

# set up the Pico W's I2C
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)

# set up BME688
bme = BreakoutBME68X(i2c, address=0x77)

def read_sensor_bme(sensor):
    global bme_exception_caught_times
    
    while True:
        try:
            return sensor.read()
        except:
            bme_exception_caught_times += 1
            time.sleep(0.5)
            pass

# change this to adjust temperature compensation
TEMPERATURE_OFFSET = 3

# these values will get updated later on
min_temperature = 100.0
max_temperature = 0.0
corrected_temperature = 0.0

for _ in range(2):
    # the gas sensor gives a few weird readings to start, lets discard them
    temperature, pressure, humidity, gas, status, _, _ = read_sensor_bme(bme)
    time.sleep(0.5)


def temperature_read():
    global corrected_temperature
    global max_temperature
    global min_temperature
    
    # read BME688
    temperature, pressure, humidity, gas, status, _, _ = read_sensor_bme(bme)

    # correct temperature and humidity using an offset
    corrected_temperature = temperature - TEMPERATURE_OFFSET

    # record min and max temperatures
    if corrected_temperature >= max_temperature:
        max_temperature = corrected_temperature
    if corrected_temperature <= min_temperature:
        min_temperature = corrected_temperature


def led_off():
    led.set_rgb(0, 0, 0)

def led_on():
    led.set_rgb(1, 1, 0)
    

def connect():
    #Connect to WLAN
    global wlan
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
        
    print_wlan()
    
    ip = wlan.ifconfig()[0]
    print(f'Connected on IP: {ip}\n')
    
    return ip


def disconnect():
    while wlan.isconnected() == True:
        print('Waiting for disconnection...')
        time.sleep(1)
        wlan.disconnect()
        
    print_wlan()


def print_wlan():
    print(f"\nWIFI is connected: {wlan.isconnected()}\n")
    print("WIFI config:")
    print(wlan.ifconfig())


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    print()
    
    return connection


def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <body style="font-size: xxx-large">
            <form action="./lighton">
            <input type="submit" value="Light on" style="width: 450px; height: 100px; font-size: xxx-large"/>
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" style="width: 450px; height: 100px; font-size: xxx-large"/>
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    
    return html


def serve():
    global client
    global connection
    
    #Start a web server
    state = 'OFF'
    # pico_led.off()
    temperature = 0
    
    while True:        
        if button_x.is_pressed:
            print("\nButton X pressed.")
            client.close()
            connection.close()
            disconnect()
            break
        
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            led_on()
            state = 'ON'
        elif request =='/lightoff?':
            led_off()
            state = 'OFF'
        
        temperature_read()
        temperature = corrected_temperature
        
        print(request)
        
        html = webpage(temperature, state)
        client.send(html)
        
        client.close()
        
        time.sleep(1)



################################

try:
    ip = connect()
    connection = open_socket(ip)
    serve()
except KeyboardInterrupt:
    machine.reset()

