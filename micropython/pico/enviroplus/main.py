import time
from machine import Pin, UART, ADC
from picographics import PicoGraphics, DISPLAY_ENVIRO_PLUS
from pimoroni import RGBLED, Button
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from pimoroni_i2c import PimoroniI2C
from breakout_ltr559 import BreakoutLTR559

# comment out the next line if no particulate sensor
from pms5003 import PMS5003

# sensors reading frequency in seconds
# value > 0s, for example 10, 2 or 0.5
SENSORS_READING_FREQUENCY = 10

# 1 is the brightest and energy consuming
# 0.5 is not very visible during a bright day
BRIGHTNESS = 0.8


"""
This example reads from all the sensors on Enviro+ and the PMS5003
particualte sensor and mic. Displays the results on screen.

Press B to turn the backlight off.
Press A to turn the backlight on for 2s every reading.
Press Y to have the screen always on (battery draining).

Saves each sensor data read, to file on Pico:
24.05.29 14:02:53;55;999;12;10.5;9;13;13;12345; 

One line takes 55 bytes on average - more if more pollution - and it can
save up to 4 days of data to Pico (theoretically), if read - as set by 
default - every 10 seconds. Then you need to remove the data from Pico, 
save it elsewhere, cause Pico has only 2MB memory. In practice better to 
do this every 24h. 


SETUP:

Go through this https://learn.pimoroni.com/article/getting-started-with-pico#installing-the-custom-firmware 

On the Releases page > under Assets, choose a stable *.uf2 file with 
*enviro* in the name. Mine is `pimoroni-enviro-v1.22.2-micropython.uf2`. 

Remember to save PMS5003 library code from
https://github.com/pimoroni/pms5003-micropython/blob/main/pms5003/__init__.py
as `pms5003.py` on your Pico. 

"""

#where to save sensor data
FILE_NAME = "sensors.txt"
COLUMN_NAMES = "date;time;temp °C;humidity %;pressure hPA;lux;average mic;pm1;pm2.5;pm10;gas;"

# change this to adjust pressure based on your altitude
# 117 for Wrocław, Poland
altitude = 117

# change this to adjust temperature compensation
TEMPERATURE_OFFSET = 3

# light the LED red if the gas reading is less than 50%
GAS_ALERT = 0.5

# screen-saving mode, with screen turning on and off to save battery
SCREEN_MODE_SAVING = "saving"
# on to have it lit all the time
SCREEN_MODE_ON = "on"
# screen off all the time to save battery
SCREEN_MODE_OFF = "off"

screen_mode = SCREEN_MODE_SAVING
mode = "sensors"

PM_PX_SIZE = 2 # change to 2 for narrower but bolder graph


def screen_on():
    display.set_backlight(BRIGHTNESS)


def screen_off():
    display.set_backlight(0)


def led_red():
    #     led.set_rgb(255, 0, 0) # too bright red
    led.set_rgb(1, 0, 0) # trying to dim led

def led_off():
    led.set_rgb(0, 0, 0)

def led_yellow():
    led.set_rgb(1, 1, 0)


def draw_gas_bar(gas, min_gas, max_gas):
    global display
    global led

    if min_gas != max_gas:
        gas_reading = (gas - min_gas) / (max_gas - min_gas)

        # light the LED and set pen to red if the gas / air quality reading is less than 50%
        if gas_reading < GAS_ALERT:
            led_red()
            display.set_pen(RED)
        else:
            led_off()
            display.set_pen(GREEN)

        percent_of_screen = round(gas_reading * SCREEN_HEIGHT)

        display.rectangle(236, SCREEN_HEIGHT - percent_of_screen, 4, percent_of_screen)
        display.text("gas", 185, 210, SCREEN_WIDTH, scale=3)


def sleep_until_next_reading():
    if screen_mode == SCREEN_MODE_SAVING and SENSORS_READING_FREQUENCY >= 2:
        print("turning off screen to save battery")
        time.sleep(2) # show the results for a moment if saving mode turned on
        screen_off() # turn off screen to save battery
        time.sleep(SENSORS_READING_FREQUENCY-2) # wait the remaining seconds
    else: # on, off
        time.sleep(SENSORS_READING_FREQUENCY)


def print_to_shell():
    print(f"{sensor_reading_date_time}")
    print(f"tem {corrected_temperature:.1f} °C")
    print(f"hum {corrected_humidity:.0f}")
    print(f"hPa {pressure_hpa:.0f}")
    print(f"lux {lux:.0f}")
    print(f"mic {mic_average_result:.1f}")
    print(f".   {data.pm_ug_per_m3(1.0):.0f}")
    print(f"o   {data.pm_ug_per_m3(2.5):.0f}")
    print(f"()  {data.pm_ug_per_m3(10):.0f}")
    print(f"gas {gas:.0f}\n")


def save_header_to_file():
    data_file = open("sensors.txt", "a")
    data_file.write(f"{COLUMN_NAMES}\n")
    data_file.close()


def save_reading_to_file():
    data_file = open("sensors.txt", "a")
    data_file.write(f"{sensor_reading_date_time};")
    data_file.write(f"{corrected_temperature:.1f};")
    data_file.write(f"{corrected_humidity:.0f};")
    data_file.write(f"{pressure_hpa:.0f};", )
    data_file.write(f"{lux:.0f};")
    data_file.write(f"{mic_average_result:.1f};")
    data_file.write(f"{data.pm_ug_per_m3(1.0):.0f};")
    data_file.write(f"{data.pm_ug_per_m3(2.5):.0f};")
    data_file.write(f"{data.pm_ug_per_m3(10):.0f};")
    data_file.write(f"{gas:.0f};\n")
    data_file.close()

    print(f"saved to file {FILE_NAME} on Pico\n")


def get_date_time_now():
    now = time.localtime()
    #         sensor_reading_time_start = time.asctime(now) # does not work
    #         sensor_reading_time_start = now.tm_year ":" now.tm_mon # does not work
    sensor_reading_date_time = "{:2d}.{:02d}.{:02d};{:02d}:{:02d}:{:02d}".format(
        now[0]-2000, now[1], now[2], now[3], now[4], now[5]) # -2000y cause less bytes

    return sensor_reading_date_time


def read_mic():
    return mic.read_u16()


def take_mic_sample(frequency, length=240):
    results = []
    for index in range(length):
        results.append(rescale_mic_result(read_mic()))
        time.sleep(1 / frequency)

    return results


def rescale_mic_result(result):
    return (result - 33100) / 30


def average(results):
    return sum(results) / len(results)


def adjust_to_sea_pressure(pressure_hpa, temperature, altitude):
    """
    Adjust pressure based on your altitude.

    credits to @cubapp https://gist.github.com/cubapp/23dd4e91814a995b8ff06f406679abcf
    """

    # Adjusted-to-the-sea barometric pressure
    adjusted_hpa = pressure_hpa + ((pressure_hpa * 9.80665 * altitude) / (287 * (273 + temperature + (altitude / 400))))
    return adjusted_hpa


def describe_pressure(pressure):
    global pressure_color

    pressure += 0.5
    if pressure < 982:
        description = "." # "very low"
    #         pressure_color = BLUE
    elif 982 <= pressure < 1004:
        description = ".." # "low"
    #         pressure_color = WHITE
    elif 1004 <= pressure < 1026:
        description = "..." # "OK"
    #         pressure_color = GREEN
    elif 1026 <= pressure < 1048:
        description = "..." # "high"
    #         pressure_color = ORANGE
    elif pressure >= 1048:
        description = "...." # "very high"
    #         pressure_color = RED

    return description


def describe_humidity(humidity):
    """Convert relative humidity into good/bad description and set color."""
    global humidity_color

    humidity += 0.5
    if humidity < 30:
        description = "." # "low"
    #         humidity_color = WHITE
    elif 30 <= humidity <= 60:
        description = ".." # "OK"
    #         humidity_color = GREEN
    elif 60 < humidity < 80:
        description = "..." # "high"
    #         humidity_color = ORANGE
    elif humidity >= 80:
        description = "...." # "very high"
    #         humidity_color = RED

    return description


def describe_light(lux):
    """Convert light level in lux to descriptive value and set color."""
    global lux_color

    lux += 0.5
    if lux < 50:
        description = "." # "dark"
    #         lux_color = GREY
    elif 50 <= lux < 100:
        description = ".." # "dim"
    #         lux_color = CYAN
    elif 100 <= lux < 500:
        description = "..." # "light"
    #         lux_color = YELLOW
    elif lux >= 500:
        description = "...." # "bright"
    #         lux_color = WHITE

    return description


def describe_mic(mic):
    """Convert mic level to descriptive value."""

    if mic < 10:
        description = "." # "quiet"
    elif 10 <= mic < 15:
        description = ".." # "noisy"
    elif 15 <= mic < 20:
        description = "..." # "loud"
    elif mic >= 20:
        description = "...." # "very loud"

    return description


def describe_temperature(temperature):
    global temperature_color

    description = ""

    if temperature <= 0:
        description = "" # "freezing"
        temperature_color = WHITE
    elif 0 < temperature <= 12:
        description = "." # "cold"
        temperature_color = BLUE
    elif 12 < temperature <= 16:
        description = ".." # "cool"
        temperature_color = GREEN
    elif 16 < temperature <= 24:
        description = "..." # "OK"
        temperature_color = YELLOW
    elif 24 < temperature <= 27:
        description = "...." # "warm"
        temperature_color = ORANGE
    elif 27 < temperature <= 33:
        description = "....." # "hot"
        temperature_color = RED
    elif temperature > 33:
        description = "......" # "very hot"
        temperature_color = PINK

    return description


def draw_pm_hist(results_array):
    result_index = 0

    for result in results_array:
        display.set_pen(PM10_COLOR)
        display.rectangle(PM_PX_SIZE * result_index, SCREEN_HEIGHT - result.pm_ug_per_m3(10), PM_PX_SIZE, SCREEN_HEIGHT)

        display.set_pen(PM25_COLOR)
        display.rectangle(PM_PX_SIZE * result_index, SCREEN_HEIGHT - result.pm_ug_per_m3(2.5), PM_PX_SIZE, SCREEN_HEIGHT)

        display.set_pen(PM1_COLOR)
        display.rectangle(PM_PX_SIZE * result_index, SCREEN_HEIGHT - result.pm_ug_per_m3(1.0), PM_PX_SIZE, SCREEN_HEIGHT)

        result_index += 1


# set up the display
display = PicoGraphics(display=DISPLAY_ENVIRO_PLUS, rotate=90)

# set up the LED
led = RGBLED(6, 7, 10, invert=True)
# led.set_brightness(50) # TODO why this does not work?

# set up the buttons
button_a = Button(12, invert=True)
button_b = Button(13, invert=True)
button_x = Button(14, invert=True)
button_y = Button(15, invert=True)

# set up the Pico W's I2C
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)

# set up BME688 and LTR559 sensors
bme = BreakoutBME68X(i2c, address=0x77)
ltr = BreakoutLTR559(i2c)

# array for storing ADC mic results
mic_results = []

# settings for bandwidth and sample size
MIC_BANDWIDTH = 2000
MIC_SAMPLE_N = 240

# setup analogue Channel for Mic
MIC_PIN = 26
mic = ADC(Pin(26))


# configure the PMS5003 for Enviro+
# comment out this section if no particulate sensor
pms5003 = PMS5003(
    uart=UART(1, tx=Pin(8), rx=Pin(9), baudrate=9600),
    pin_enable=Pin(3),
    pin_reset=Pin(2),
    mode="active"
)

# some constants we'll use for drawing
BLACK = display.create_pen(0, 0, 0)
GREY = display.create_pen(75, 75, 75)
WHITE = display.create_pen(255, 255, 255)
BLUE = display.create_pen(0, 0, 200)
CYAN = display.create_pen(0, 200, 255)
GREEN = display.create_pen(0, 255, 0)
YELLOW = display.create_pen(255, 220, 0)
ORANGE = display.create_pen(255, 185, 0)
RED = display.create_pen(255, 0, 0)
PINK = display.create_pen(255, 62, 165)
MAGENTA = display.create_pen(200, 0, 200)

FFT_COLOUR = display.create_pen(255, 0, 255)

PM1_COLOR = CYAN
PM25_COLOR = PINK
PM10_COLOR = YELLOW

DEFAULT = WHITE


temperature_color = DEFAULT
humidity_color = DEFAULT
pressure_color = DEFAULT
lux_color = DEFAULT
mic_color = DEFAULT
pm1_color = DEFAULT
pm25_color = DEFAULT
pm10_color = DEFAULT
gas_color = DEFAULT



SCREEN_WIDTH, SCREEN_HEIGHT = display.get_bounds()
print(f"display width: {SCREEN_WIDTH}")
print(f"display height: {SCREEN_HEIGHT}\n")

display.set_font("bitmap8")

# these values will get updated later on
min_temperature = 100.0
max_temperature = 0.0
min_gas = 100000.0
max_gas = 0.0

# array for storing particulate readings
results_particulates = []

# setup
led_yellow()
screen_on()
display.set_pen(YELLOW)
display.text("waiting for sensors", 0, 0, SCREEN_WIDTH, scale=5)
display.update()


def read_sensor(sensor):
    while True:
        try:
            return sensor.read()
        except:
            pass
        

for _ in range(2):
    # the gas sensor gives a few weird readings to start, lets discard them
    temperature, pressure, humidity, gas, status, _, _ = read_sensor(bme)
    read_sensor(pms5003)
    time.sleep(0.5)

#prep sensor readings file to write to it
save_header_to_file()


while True:

    # turn on the backlight with A and turn it back off with B
    # switch between sensor and equaliser mode with X and Y
    if button_a.is_pressed:
        screen_mode = SCREEN_MODE_ON
    elif button_b.is_pressed:
        screen_mode = SCREEN_MODE_SAVING
    elif button_y.is_pressed:
        screen_mode = SCREEN_MODE_OFF

    if screen_mode == SCREEN_MODE_SAVING or screen_mode == SCREEN_MODE_ON:
        screen_on()
        time.sleep(0.2)
    elif screen_mode == SCREEN_MODE_OFF:
        screen_off()
        time.sleep(0.2)

    if mode == "sensors":

        #time start
        sensor_reading_date_time = get_date_time_now()

        #read mic
        mic_results = take_mic_sample(MIC_BANDWIDTH, MIC_SAMPLE_N)
        #         mic_max_result = max(mic_results)
        mic_average_result = average(mic_results)

        # read BME688
        temperature, pressure, humidity, gas, status, _, _ = read_sensor(bme)
        heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"

        # correct temperature and humidity using an offset
        corrected_temperature = temperature - TEMPERATURE_OFFSET
        dewpoint = temperature - ((100 - humidity) / 5)
        corrected_humidity = 100 - (5 * (corrected_temperature - dewpoint))

        # record min and max temperatures
        if corrected_temperature >= max_temperature:
            max_temperature = corrected_temperature
        if corrected_temperature <= min_temperature:
            min_temperature = corrected_temperature

        # record min and max gas readings
        if gas > max_gas:
            max_gas = gas
        if gas < min_gas:
            min_gas = gas

        # convert pressure into hpa
        pressure_hpa = pressure / 100

        # correct pressure
        pressure_hpa = adjust_to_sea_pressure(pressure_hpa, corrected_temperature, altitude)

        # read LTR559
        ltr_reading = ltr.get_reading()
        lux = ltr_reading[BreakoutLTR559.LUX]
        prox = ltr_reading[BreakoutLTR559.PROXIMITY]

        # read particulate sensor and put the results into an array
        # comment out if no PM sensor
        data = read_sensor(pms5003)
        results_particulates.append(data)
        if (len(results_particulates) > SCREEN_WIDTH / PM_PX_SIZE):  # scroll the result list by removing the first value
            results_particulates.pop(0)

        if heater == "Stable" and ltr_reading is not None:
            led_off()

            # draw some stuff on the screen
            display.set_pen(BLACK)
            display.clear()

            # draw on bottom of screen the particulate graph on screen
            # comment out if no PM sensor
            draw_pm_hist(results_particulates)

            # draw the top box
            display.set_pen(GREY)
            display.rectangle(0, 0, SCREEN_WIDTH, 60)

            # pick a pen colour based on the temperature
            display.set_pen(DEFAULT)
            describe_temperature(corrected_temperature)
            display.set_pen(temperature_color)
            display.text(f"{corrected_temperature:.1f}°C", 5, 	15, SCREEN_WIDTH, scale=4)

            # draw temp max and min
            display.set_pen(DEFAULT)
            display.text(f"min {min_temperature:.1f}", 125, 	5, SCREEN_WIDTH, scale=2)
            display.text(f"max {max_temperature:.1f}", 125, 	30, SCREEN_WIDTH, scale=3)

            # draw the first column of text
            display.set_pen(DEFAULT)
            display.text(f"hum {corrected_humidity:.0f}%", 0, 	75, SCREEN_WIDTH, scale=2)
            display.text(f"hPa {pressure_hpa:.0f}", 0, 			100, SCREEN_WIDTH, scale=2)
            display.text(f"lux {lux:.0f}", 0, 					125, SCREEN_WIDTH, scale=2)

            display.set_pen(PM1_COLOR)
            display.text(f"pm1   {data.pm_ug_per_m3(1.0):.0f}", 0, 150, SCREEN_WIDTH, scale=2)
            display.set_pen(PM25_COLOR)
            display.text(f"pm2.5 {data.pm_ug_per_m3(2.5):.0f}", 0, 175, SCREEN_WIDTH, scale=2)
            display.set_pen(PM10_COLOR)
            display.text(f"pm10  {data.pm_ug_per_m3(10):.0f}", 0, 	200, SCREEN_WIDTH, scale=2)

            # draw the second column of text
            humidity_describe = describe_humidity(corrected_humidity)
            display.set_pen(humidity_color)
            display.text(f"{humidity_describe}", 100, 	75, SCREEN_WIDTH, scale=2)

            pressure_describe=describe_pressure(pressure_hpa)
            display.set_pen(pressure_color)
            display.text(f"{pressure_describe}", 100, 		100, SCREEN_WIDTH, scale=2)

            lux_describe = describe_light(lux)
            display.set_pen(lux_color)
            display.text(f"{lux_describe}", 100, 					125, SCREEN_WIDTH, scale=2)

            display.set_pen(mic_color)
            display.text(f"mic: {mic_average_result:.1f}", 100, 	175, SCREEN_WIDTH, scale=2)

            # print to shell
            print_to_shell()

            # draw bar for gas
            draw_gas_bar(gas, min_gas, max_gas)

            #show results on screen
            display.update()

            # save to file
            save_reading_to_file()

            # wait for next reading
            sleep_until_next_reading()
