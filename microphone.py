# Mikrofon modul til TaskManager
# Måler lydniveau via INMP441 I2S mikrofon

from machine import I2S, Pin
import math
import array


# =====================================================
# CONFIG
# =====================================================

# Hvor ofte mikrofon tasken køres
MIC_TASK_INTERVAL_MS = 50

# Antal lyd samples der læses pr. måling
# Flere samples giver mere stabile målinger
SAMPLES_NUM = 128


# =====================================================
# I2S MICROPHONE SETUP
# =====================================================

# Opretter I2S forbindelse til INMP441 mikrofonen
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

    # INMP441 bruger 32-bit frames
    bits=32,

    # Mono lyd
    format=I2S.MONO,

    # Sample rate
    # 16000 samples pr sekund
    rate=16000,

    # Intern buffer til I2S driveren
    ibuf=2048,
)


# =====================================================
# BUFFER
# =====================================================

# Buffer til lyddata
# array('i') betyder signed 32-bit integers
buffer = array.array('i', [0] * SAMPLES_NUM)


# =====================================================
# VARIABLES
# =====================================================

# Endeligt lydniveau i dB
sound_level = 0

# Bruges til smoothing/filtering
smoothed_level = 0


# =====================================================
# INIT
# =====================================================

# Init funktion
# Bruges hvis modulet senere skal konfigureres
def mic_init():
    pass


# =====================================================
# GETTERS
# =====================================================

# Returnerer det aktuelle lydniveau
def get_sound_level():

    return sound_level


# =====================================================
# SOUND CALCULATION
# =====================================================

# Beregner nyt lydniveau ud fra mikrofon data
def calculate_sound_level():

    global sound_level
    global smoothed_level


    # =====================================================
    # READ MICROPHONE DATA
    # =====================================================

    # Læser lyddata ind i buffer
    bytes_read = audio_in.readinto(buffer)


    # Stop hvis ingen data blev læst
    if bytes_read == 0:
        return


    # Antal samples i bufferen
    sample_count = len(buffer)


    # =====================================================
    # DC OFFSET REMOVAL
    # =====================================================

    # Mange mikrofoner har et DC offset
    # Signalets gennemsnit ligger derfor ikke præcist omkring 0
    # Dette kan give forkerte RMS og dB målinger
    # Derfor beregnes gennemsnittet og fjernes fra signalet

    total_sum = 0


    # Beregn gennemsnit af alle samples
    for sample in buffer:

        # Shift reducerer størrelsen på værdierne
        # INMP441 sender store 32-bit værdier
        total_sum += (sample >> 14)


    # Beregn gennemsnitlig offset
    mean_offset = total_sum / sample_count


    # =====================================================
    # RMS CALCULATION
    # =====================================================

    # RMS bruges til at beregne lydsignalets styrke

    total_squares = 0


    for sample in buffer:

        # Fjern DC offset fra sample
        actual_sample = (sample >> 14) - mean_offset

        # Kvadrer sample til RMS beregning
        total_squares += (
            actual_sample * actual_sample
        )


    # Beregn RMS værdi
    rms = math.sqrt(
        total_squares / sample_count
    )


    # =====================================================
    # dB CALCULATION
    # =====================================================

    # Undgår math fejl ved log10(0)
    if rms < 0.01:
        rms = 0.01


    # Reference værdi til dB beregning
    # Justeres ved kalibrering
    REFERENCE = 450.0


    # Beregn relativ dB værdi
    level = 20 * math.log10(
        rms / REFERENCE
    )


    # Offset gør værdierne mere realistiske
    level += 40


    # =====================================================
    # LIMIT VALUES
    # =====================================================

    # Forhindrer urealistiske værdier

    if level < 15:
        level = 15

    if level > 120:
        level = 120


    # =====================================================
    # SMOOTHING
    # =====================================================

    # Smoothing reducerer hurtige udsving
    # og giver mere stabile miljømålinger

    smoothed_level = (

        (smoothed_level * 0.97)

        +

        (level * 0.03)
    )


    # =====================================================
    # SAVE FINAL VALUE
    # =====================================================

    sound_level = smoothed_level


# =====================================================
# TASK
# =====================================================

# Task funktion som kaldes af TaskManager
def microphone_task():

    calculate_sound_level()


# =====================================================
# DEBUG TASK
# =====================================================

# Printer lydniveau til terminal
def debug_task():

    print(
        f"Lydniveau: {sound_level:.1f} dB"
    )