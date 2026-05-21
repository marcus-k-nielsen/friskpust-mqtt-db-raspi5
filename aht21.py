# AHT21 modul til TaskManager
# Måler temperatur og luftfugtighed
# SDA=GPIO4, SCL=GPIO5, VCC=3.3V, GND=GND
from machine import I2C, Pin

# I2C setup
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)

# Intevaller
TASK_INTERVAL_MS = 100 # Hvor ofte TaskManageren kalder C_ENS160_Task() i ms
READ_INTERVAL_MS = 5000 # Hvor ofte der faktisk læses data fra AHT21 i ms
WAIT_INTERVAL_MS = 80 # Vent 80 ms på at AHT21 færdiggør målingen, før data læses

# Tilstande
STATE_IDLE = 0 # Venter på næste målingstidspunkt
STATE_TRIGGER = 1 # Send målingskommando til sensor
STATE_WAITING = 2 # Venter på at sensor er klar med data
STATE_READ = 3 # Læser data fra sensor


# Variabler
read_timer_ms = 0 # Tæller hvor mange ms der er gået siden sidste læsning af AHT21
wait_timer_ms = 0 # Tæller hvor mange ms der er gået siden startkommando blev sendt til AHT21
state = STATE_IDLE # Gemmer nuværende tilstand i state machine
temperature_c = 0.0 # Gemmer seneste temperaturmåling i °C
relative_humidity_pct = 0.0 # Gemmer seneste luftfugtighedsmåling i %RH


# Private funktioner
def _aht21_read():
    raw_byte = i2c.readfrom(0x38, 6)

    # Pak rå bytes ud til heltal
    raw_relative_humidity = (raw_byte[1] << 12) | (raw_byte[2] << 4) | (raw_byte[3] >> 4)
    raw_temperature = ((raw_byte[3] & 0x0F) << 16) | (raw_byte[4] << 8) | raw_byte[5]

    # Omregn til procent og grader
    relative_humidity = raw_relative_humidity / 2**20 * 100
    temperature = raw_temperature / 2**20 * 200 - 50

    return temperature, relative_humidity


# Public funktioner
def aht21_init():
   pass
    
def aht21_task():
    global read_timer_ms, wait_timer_ms, state, temperature_c, relative_humidity_pct
 
    if state == STATE_IDLE:
        if read_timer_ms >= READ_INTERVAL_MS:
            read_timer_ms = 0
            state = STATE_TRIGGER
        else:
            read_timer_ms += TASK_INTERVAL_MS
 
    elif state == STATE_TRIGGER:
        i2c.writeto(0x38, bytes([0xAC, 0x33, 0x00])) # Beder AHT21 om en ny måling
        wait_timer_ms = 0
        state = STATE_WAITING
 
    elif state == STATE_WAITING:
        if wait_timer_ms >= WAIT_INTERVAL_MS:
            state = STATE_READ
        else:
            wait_timer_ms += TASK_INTERVAL_MS
 
    elif state == STATE_READ:
        temperature_c, relative_humidity_pct = _aht21_read() # Kalder _aht21_read() funktionen som læser og omregner data fra AHT21
        print(f"Temp: {temperature_c:.1f}°C  RH: {relative_humidity_pct:.1f}%")
        state = STATE_IDLE


def aht21_get_data(): # Returnerer seneste måling af temperatur og luftfugtighed, uden at bryde loggikken i C_AHT21_Task()
    return temperature_c, relative_humidity_pct
