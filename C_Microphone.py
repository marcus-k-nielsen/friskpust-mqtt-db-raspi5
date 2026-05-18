# Mikrofon modul til TaskManager
# Måler lydniveau via INMP441 I2S mikrofon

from machine import I2S, Pin
import struct
import math


# Hvor ofte mikrofon tasken køres
MIC_TASK_INTERVAL_MS = 50


# Opretter I2S forbindelse til mikrofonen
audio_in = I2S(

    # I2S bus nummer
    0,

    # Clock signal
    sck=Pin(16),

    # Word select signal
    ws=Pin(17),

    # Data signal fra mikrofonen
    sd=Pin(18),

    # RX betyder at Picoen modtager data
    mode=I2S.RX,

    # 16-bit lyd samples
    bits=16,

    # Mono lyd
    format=I2S.MONO,

    # 16000 samples per sekund
    rate=16000,

    # Intern buffer til I2S driveren
    ibuf=2000,
)


# Buffer til lyddata
# Mikrofon samples læses ind her
buf = bytearray(256)


# Variabel som gemmer det færdige lydniveau
iSoundLevel = 0

# Variabel til smoothing/filtering
fSmoothedLevel = 0


# Init funktion
# Bruges til fremtidig setup eller konfiguration
def C_MIC_Init():
    pass


# Returnerer det aktuelle lydniveau
def C_MIC_GetSoundLevel():

    return iSoundLevel


# Beregner nyt lydniveau ud fra mikrofon data
def C_MIC_Calculate():

    global iSoundLevel
    global fSmoothedLevel


    # Bruges til RMS beregning
    total = 0

    # Antal samples
    samples = 0


    # Læser lyddata ind i bufferen
    audio_in.readinto(buf)


    # Gennemgår bufferen 2 bytes ad gangen
    # 16-bit = 2 bytes
    for i in range(0, len(buf), 2):


        # Konverterer rå bytes til signed 16-bit tal
        sample = struct.unpack(
            "<h",
            buf[i:i+2]
        )[0]


        # Kvadrerer sample til RMS beregning
        total += sample * sample

        # Tæller antal samples
        samples += 1


    # Beregner RMS lydniveau
    rms = math.sqrt(total / samples)


    # Software gain / sensitivitet
    level = rms / 3


    # Fjerner baggrundsstøj og små udsving
    level = level - 100


    # Sikrer at lydniveau ikke bliver negativt
    if level < 0:
        level = 0


    # Smoothing gør værdierne mere stabile
    fSmoothedLevel = (
        (fSmoothedLevel * 0.95)
        + (level * 0.05)
    )


    # Gemmer det endelige lydniveau
    iSoundLevel = int(fSmoothedLevel)


# Task funktion som kaldes af TaskManageren
def C_MIC_Task():

    C_MIC_Calculate()


# Debug task som printer lydniveauet
def C_Debug_Task():

    print(C_MIC_GetSoundLevel())