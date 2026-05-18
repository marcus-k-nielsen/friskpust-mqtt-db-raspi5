# C_Microphone.py

from machine import I2S, Pin
import struct
import math

# =========================
# CONFIG
# =========================

MIC_TASK_INTERVAL_MS = 50

# =========================
# HARDWARE
# =========================

audio_in = I2S(
    0,
    sck=Pin(16),
    ws=Pin(17),
    sd=Pin(18),
    mode=I2S.RX,
    bits=16,
    format=I2S.MONO,
    rate=16000,
    ibuf=2000,
)

buf = bytearray(256)

# =========================
# VARIABLES
# =========================

iSoundLevel = 0
fSmoothedLevel = 0

# =========================
# INIT
# =========================

def C_MIC_Init():
    pass

# =========================
# GETTERS
# =========================

def C_MIC_GetSoundLevel():
    return iSoundLevel

# =========================
# CALCULATE
# =========================

def C_MIC_Calculate():

    global iSoundLevel
    global fSmoothedLevel

    total = 0
    samples = 0

    audio_in.readinto(buf)

    for i in range(0, len(buf), 2):

        sample = struct.unpack("<h", buf[i:i+2])[0]

        total += sample * sample
        samples += 1

    rms = math.sqrt(total / samples)

    # Gain
    level = rms / 3

    # Remove baseline noise
    level = level - 100

    if level < 0:
        level = 0

    # Smoothing
    fSmoothedLevel = (fSmoothedLevel * 0.95) + (level * 0.05)

    iSoundLevel = int(fSmoothedLevel)

# =========================
# TASK
# =========================

def C_MIC_Task():

    C_MIC_Calculate()

# =========================
# DEBUG TASK
# =========================

def C_Debug_Task():

    print(C_MIC_GetSoundLevel())   