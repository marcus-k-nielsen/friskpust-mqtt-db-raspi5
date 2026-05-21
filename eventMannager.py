# Event manager modul
# Håndterer thresholds, states og event detection

from microphone import *
from aht21 import *

import ujson


# =====================================================
# SOUND STATES
# =====================================================

STATE_SOUND_QUIET = 0
STATE_SOUND_GOOD = 1
STATE_SOUND_LOUD = 2
STATE_SOUND_VERY_LOUD = 3


# =====================================================
# TEMPERATURE STATES
# =====================================================

STATE_TEMP_TOO_COLD = 0
STATE_TEMP_COLD = 1
STATE_TEMP_GOOD = 2
STATE_TEMP_GREAT = 3
STATE_TEMP_HOT = 4


# =====================================================
# HUMIDITY STATES
# =====================================================

STATE_HUMIDITY_LOW = 0
STATE_HUMIDITY_GOOD = 1
STATE_HUMIDITY_HIGH = 2


# =====================================================
# ECO2 STATES
# =====================================================

STATE_ECO2_GOOD = 0
STATE_ECO2_BAD = 1


# =====================================================
# CURRENT STATES
# =====================================================

sound_state = STATE_SOUND_GOOD
temp_state = STATE_TEMP_GOOD
humidity_state = STATE_HUMIDITY_GOOD
eco2_state = STATE_ECO2_GOOD

# =====================================================
# CHECK EVENTS
# =====================================================

def check_events():

    global sound_state
    global temp_state
    global humidity_state
    global eco2_state
    
    should_publish = False


    # =====================================================
    # GET SENSOR VALUES
    # =====================================================

    sound = get_sound_level()

    temperature, humidity = aht21_get_data()


    # =====================================================
    # SOUND STATES
    # =====================================================

    previous_sound_state = sound_state


    # Under 30 dB
    if sound < 30:

        sound_state = STATE_SOUND_QUIET

    # 30 dB -> 40 dB
    elif sound < 40:
        sound_state = STATE_SOUND_GOOD

    # 40 dB -> 80 dB
    elif sound < 80:
        sound_state = STATE_SOUND_LOUD

    # Over 80 dB
    else:
        sound_state = STATE_SOUND_VERY_LOUD


    # Publish hvis state ændres
    if sound_state != previous_sound_state:

        print("EVENT: SOUND STATE CHANGED")

        should_publish = True


    # =====================================================
    # TEMPERATURE STATES
    # =====================================================

    previous_temp_state = temp_state


    # Under 17.5°C
    if temperature < 17.5:

        temp_state = STATE_TEMP_TOO_COLD


    # 17.5°C -> 19.5°C
    elif temperature < 19.5:

        temp_state = STATE_TEMP_COLD


    # 19.5°C -> 21.5°C
    elif temperature < 21.5:

        temp_state = STATE_TEMP_GOOD


    # 21.5°C -> 24.5°C
    elif temperature < 24.5:

        temp_state = STATE_TEMP_GREAT


    # Over 24.5°C
    else:

        temp_state = STATE_TEMP_HOT


    # Publish hvis state ændres
    if temp_state != previous_temp_state:
        print("EVENT: TEMP STATE CHANGED")
        should_publish = True


    # =====================================================
    # HUMIDITY STATES
    # =====================================================

    previous_humidity_state = humidity_state


    # Under 40%
    if humidity < 40:

        humidity_state = STATE_HUMIDITY_LOW


    # 40% -> 65%
    elif humidity <= 65:

        humidity_state = STATE_HUMIDITY_GOOD


    # Over 65%
    else:

        humidity_state = STATE_HUMIDITY_HIGH


    # Publish hvis state ændres
    if humidity_state != previous_humidity_state:

        print("EVENT: HUMIDITY STATE CHANGED")

        should_publish = True


    # =====================================================
    # ECO2 STATES
    # =====================================================

    iPreviousEco2State = iEco2State


    # Over 0.1%
    if fEco2 > 0.1:

        iEco2State = STATE_ECO2_BAD


    # Under 0.1%
    else:

        iEco2State = STATE_ECO2_GOOD


    # Publish hvis state ændres
    if iEco2State != iPreviousEco2State:

        print("EVENT: ECO2 STATE CHANGED")

        print(
            "Old:",
            iPreviousEco2State,
            "New:",
            iEco2State
        )

        bPublish = True


    return should_publish


# =====================================================
# CREATE PAYLOAD
# =====================================================

def create_payload():
    sound = get_sound_level()

    temperature, humidity = aht21_get_data()


    payload = {

        # Sensor værdier
        "temperature": temperature,
        "humidity": humidity,
        "sound": sound
    }


    return ujson.dumps(payload)