# Event manager modul
# Håndterer thresholds, states og event detection

from microphone import *
from aht21 import *
from ens160 import *

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

    eco2 = ens160_get_eco2()


    # =====================================================
    # SOUND STATES
    # =====================================================

    previous_sound_state = sound_state


    if sound < 30:

        sound_state = STATE_SOUND_QUIET

    elif sound < 40:

        sound_state = STATE_SOUND_GOOD

    elif sound < 80:

        sound_state = STATE_SOUND_LOUD

    else:

        sound_state = STATE_SOUND_VERY_LOUD


    if sound_state != previous_sound_state:

        print("EVENT: SOUND STATE CHANGED")

        should_publish = True


    # =====================================================
    # TEMPERATURE STATES
    # =====================================================

    previous_temp_state = temp_state


    if temperature < 17.5:

        temp_state = STATE_TEMP_TOO_COLD

    elif temperature < 19.5:

        temp_state = STATE_TEMP_COLD

    elif temperature < 21.5:

        temp_state = STATE_TEMP_GOOD

    elif temperature < 24.5:

        temp_state = STATE_TEMP_GREAT

    else:

        temp_state = STATE_TEMP_HOT


    if temp_state != previous_temp_state:

        print("EVENT: TEMP STATE CHANGED")

        should_publish = True


    # =====================================================
    # HUMIDITY STATES
    # =====================================================

    previous_humidity_state = humidity_state


    if humidity < 40:

        humidity_state = STATE_HUMIDITY_LOW

    elif humidity <= 65:

        humidity_state = STATE_HUMIDITY_GOOD

    else:

        humidity_state = STATE_HUMIDITY_HIGH


    if humidity_state != previous_humidity_state:

        print("EVENT: HUMIDITY STATE CHANGED")

        should_publish = True


    # =====================================================
    # ECO2 STATES
    # =====================================================

    previous_eco2_state = eco2_state


    # Under 1000 ppm
    if eco2 < 1000:

        eco2_state = STATE_ECO2_GOOD


    # Over 1000 ppm
    else:

        eco2_state = STATE_ECO2_BAD


    if eco2_state != previous_eco2_state:

        print("EVENT: ECO2 STATE CHANGED")

        should_publish = True


    return should_publish


# =====================================================
# CREATE PAYLOAD
# =====================================================

def create_payload():

    sound = get_sound_level()

    temperature, humidity = aht21_get_data()

    eco2 = ens160_get_eco2()


    payload = {

        "temperature": temperature,
        "humidity": humidity,
        "sound": sound,
        "eco2": eco2
    }


    return ujson.dumps(payload)