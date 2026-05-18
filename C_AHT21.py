# AHT21 modul til TaskManager
# Måler temperatur og relativ luftfugtighed via I2C

from machine import I2C, Pin


# Opretter I2C forbindelse på bus 0
# SDA = GPIO4
# SCL = GPIO5
# freq bestemmer kommunikationshastigheden
i2c = I2C(
    0,
    sda=Pin(4),
    scl=Pin(5),
    freq=100_000
)


# Hvor ofte tasken køres af TaskManageren
AHT21_TASK_INTERVAL_MS = 100

# Hvor ofte der skal startes en ny måling
AHT21_READ_INTERVAL_MS = 5000

# Ventetid på at sensoren bliver færdig med målingen
AHT21_WAIT_INTERVAL_MS = 80


# States til state maskinen
STATE_IDLE = 0
STATE_TRIGGER = 1
STATE_WAITING = 2
STATE_READ = 3


# Timer variabler
iReadTimer_ms = 0
iWaitTimer_ms = 0

# Aktuel state
iState = STATE_IDLE

# Gemmer seneste temperatur og luftfugtighed
iTemp_C = 0.0
iRh_pct = 0.0


# Privat hjælpefunktion til at læse rå data fra sensoren
def _aht21_read():

    # Læser 6 bytes fra AHT21 sensoren
    d = i2c.readfrom(0x38, 6)

    # Konverterer rå luftfugtighedsdata til procent
    rh = (
        ((d[1] << 12) | (d[2] << 4) | (d[3] >> 4))
        / 2**20
        * 100
    )

    # Konverterer rå temperaturdata til grader Celsius
    temp = (
        (((d[3] & 0x0F) << 16) | (d[4] << 8) | d[5])
        / 2**20
        * 200
        - 50
    )

    return temp, rh


# Init funktion
# Bruges til fremtidig setup eller konfiguration
def C_AHT21_Init():
    pass


# Task funktion som styres af TaskManageren
def C_AHT21_Task():

    global iReadTimer_ms
    global iWaitTimer_ms
    global iState
    global iTemp_C
    global iRh_pct


    # IDLE state
    # Venter indtil næste måling skal startes
    if iState == STATE_IDLE:

        if iReadTimer_ms >= AHT21_READ_INTERVAL_MS:

            iReadTimer_ms = 0
            iState = STATE_TRIGGER

        else:

            iReadTimer_ms += AHT21_TASK_INTERVAL_MS


    # TRIGGER state
    # Sender kommando til sensoren om at starte måling
    elif iState == STATE_TRIGGER:

        i2c.writeto(
            0x38,
            bytes([0xAC, 0x33, 0x00])
        )

        iWaitTimer_ms = 0
        iState = STATE_WAITING


    # WAITING state
    # Venter på at sensoren bliver færdig med målingen
    elif iState == STATE_WAITING:

        if iWaitTimer_ms >= AHT21_WAIT_INTERVAL_MS:

            iState = STATE_READ

        else:

            iWaitTimer_ms += AHT21_TASK_INTERVAL_MS


    # READ state
    # Læser målingen og gemmer værdierne
    elif iState == STATE_READ:

        iTemp_C, iRh_pct = _aht21_read()

        print(
            f"Temp: {iTemp_C:.1f}°C  RH: {iRh_pct:.1f}%"
        )

        iState = STATE_IDLE


# Returnerer seneste målte data
def C_AHT21_GetData():

    return iTemp_C, iRh_pct