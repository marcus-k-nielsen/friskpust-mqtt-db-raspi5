# AHT21 modul til TaskManager
# Måler temperatur og luftfugtighed
# SDA=GPIO4, SCL=GPIO5, VCC=3.3V, GND=GND

from machine import I2C, Pin

###################################################################################################
# Hardware config
###################################################################################################
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)

###################################################################################################
# Name definitions
###################################################################################################
AHT21_TASK_INTERVAL_MS = 100 # Hvor ofte TaskManageren kalder C_ENS160_Task() i ms
AHT21_READ_INTERVAL_MS = 5000 # Hvor ofte der faktisk læses data fra AHT21 i ms
AHT21_WAIT_INTERVAL_MS = 80 # Vent 80 ms efter startkommando på at sensor færdiggør målingen

STATE_IDLE = 0 # Venter på næste målingstidspunkt
STATE_TRIGGER = 1 # Send målingskommando til sensor
STATE_WAITING = 2 # Venter på at sensor er klar med data
STATE_READ = 3 # Læser data fra sensor

###################################################################################################
# Local variables
###################################################################################################
iReadTimer_ms = 0 # Tæller hvor mange ms der er gået siden sidste læsning af AHT21
iWaitTimer_ms = 0 # Tæller hvor mange ms der er gået siden startkommando blev sendt til AHT21
iState        = STATE_IDLE # Gemmer nuværende tilstand i state machine
iTemp_C       = 0.0 # Gemmer seneste temperaturmåling i °C
iRh_pct       = 0.0 # Gemmer seneste luftfugtighedsmåling i %RH

###################################################################################################
# Private functions
###################################################################################################
def _aht21_read():
    d    = i2c.readfrom(0x38, 6)
    rh   = ((d[1] << 12) | (d[2] << 4) | (d[3] >> 4)) / 2**20 * 100
    temp = (((d[3] & 0x0F) << 16) | (d[4] << 8) | d[5]) / 2**20 * 200 - 50
    return temp, rh

###################################################################################################
# Public functions
###################################################################################################

def C_AHT21_Init():
    pass


def C_AHT21_Task():
    global iReadTimer_ms, iWaitTimer_ms, iState, iTemp_C, iRh_pct
 
    if iState == STATE_IDLE:
        if iReadTimer_ms >= AHT21_READ_INTERVAL_MS:
            iReadTimer_ms = 0
            iState = STATE_TRIGGER
        else:
            iReadTimer_ms += AHT21_TASK_INTERVAL_MS
 
    elif iState == STATE_TRIGGER:
        i2c.writeto(0x38, bytes([0xAC, 0x33, 0x00])) # Beder AHT21 om en ny måling
        iWaitTimer_ms = 0
        iState = STATE_WAITING
 
    elif iState == STATE_WAITING:
        if iWaitTimer_ms >= AHT21_WAIT_INTERVAL_MS:
            iState = STATE_READ
        else:
            iWaitTimer_ms += AHT21_TASK_INTERVAL_MS
 
    elif iState == STATE_READ:
        iTemp_C, iRh_pct = _aht21_read() # Kalder _aht21_read() funktionen som læser og omregner data fra AHT21
        print(f"Temp: {iTemp_C:.1f}°C  RH: {iRh_pct:.1f}%")
        iState = STATE_IDLE


def C_AHT21_GetData(): # Returnerer seneste måling af temperatur og luftfugtighed, uden at bryde loggikken i C_AHT21_Task()
    return iTemp_C, iRh_pct
