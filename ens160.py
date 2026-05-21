# ENS160 modul til TaskManager
# Måler eCO2 – bruger AHT21-data til kompensation
# SDA=GPIO4, SCL=GPIO5, VCC=3.3V, GND=GND

from machine import I2C, Pin
import time
import aht21

# Hardware config
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)

# Intevaller
TASK_INTERVAL_MS = 100
READ_INTERVAL_MS = 5000

# Tilstande
STATE_IDLE        = 0   # Venter på næste måling
STATE_COMPENSATE  = 1   # Send temp/RH kompensation til sensor
STATE_READ        = 2   # Læs eCO2 fra sensor

# Variabler
read_timer_ms = 0
state        = STATE_IDLE
eco2_ppm     = 0


# Private funktioner
def _wr(reg, data): # 0x53 er ENS160 I2C adresse, reg er registeradresse, data er byte eller liste af bytes der skal skrives til registeret.
    if isinstance(data, list): 
        i2c.writeto_mem(0x53, reg, bytes(data)) # Skriver til ENS160 register, og tjekker om data er en liste eller enkelt byte
    else:
        i2c.writeto_mem(0x53, reg, bytes([data])) # hvis det er en enkelt byte, pakker den ind i en liste.

def _rd(reg, n=1): # Læser n bytes fra ENS160 register over i2c, og returnerer det som bytes. Standard er 1 byte, men kan specificeres ved at sende n som argument.
    return i2c.readfrom_mem(0x53, reg, n)


# Public funktioner
def ens160_init():
    _wr(0x10, 0xF0)     # 0x10 er ENS160 styreregister --> 0xF0 resetkommando
    time.sleep_ms(100)
    _wr(0x10, 0x02)     # 0x10 er ENS160 styreregister --> 0x02 start standard måletilstand
    time.sleep_ms(50)

def task():
    global read_timer_ms, state, eco2_ppm

    if state == STATE_IDLE:
        if read_timer_ms >= READ_INTERVAL_MS:
            read_timer_ms = 0
            state = STATE_COMPENSATE
        else:
            read_timer_ms += TASK_INTERVAL_MS

    elif state == STATE_COMPENSATE:
        temp, rh = aht21.get_data() # Data hentes fra AHT21 modulet, og gemmes i temp og rh variablerne
        # ENS160 forventer temperatur i Kelvin, der omregnes fra Celsius til Kelvin, og skaleres op med 64 for at få det i det format ENS160 kræver. (Afrunding sker ved at konvertere til int)
        t_raw  = int((temp + 273.15) * 64) 
        # Talet skal pakkes ned og fordeles i 2 bytes, da ENS160 forventer det i det format. Det gøres ved at bruge bitmanipulation til at få low og high byte.
        t_low     = t_raw & 0xFF    # Beholder de 8 mindste bits for low byte
        t_high    = t_raw >> 8      # Skifter bits 8 pladser til højre for at få high byte (de 8 mest signifikante bits) --> (længst til venstre, og dermed højst positionelle værdi)

        # Omregn luftfugtighed til %RH * 512 (ENS160 format)
        rh_raw    = int(rh * 512)
        rh_low    = rh_raw & 0xFF
        rh_high   = rh_raw >> 8

        # De 2 kompensationsværdier skrives til ENS160, og derefter skifter state til STATE_READ for at læse eCO2 i næste iteration
        _wr(0x13, [t_low, t_high])      # 0x13 er ENS160 register for temperaturkompensation
        _wr(0x15, [rh_low, rh_high])    # 0x15 er ENS160 register for luftfugtighedskompensation
        state = STATE_READ

    elif state == STATE_READ:  # Henter seneste eCO2 måling fra ENS160 (ved hjælp af _rd funktionen), og konverterer det fra bytes til int ved at specificere 'little' endian format, da ENS160 sender data i det format.
        eco2_ppm = int.from_bytes(_rd(0x24, 2), 'little') # int.from_bytes() konverterer byte data til int, og specificerer at byte rækkefølgen er 'little' endian (mindste byte først). Ex: low byte * 256 + high byte (Der arbjedes kun med 2 bytes, da eCO2 data er 16-bit --> 256 er konstanten for at flytte high byte til dets korrekte position i det endelige tal)
        print(f"eCO2: {eco2_ppm}ppm")
        state = STATE_IDLE

def get_eco2():
    return eco2_ppm