# Event manager modul
# Håndterer thresholds, states og event detection

from C_Microphone import *
from C_AHT21 import *

import ujson


# =====================================================
# SOUND STATES
# =====================================================

STATE_SOUND_VERY_LOW = 0
STATE_SOUND_GOOD = 1
STATE_SOUND_HIGH = 2
STATE_SOUND_VERY_HIGH = 3


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

iSoundState = STATE_SOUND_GOOD

iTempState = STATE_TEMP_GOOD

iHumidityState = STATE_HUMIDITY_GOOD

iEco2State = STATE_ECO2_GOOD


# =====================================================
# PLACEHOLDER VALUE
# =====================================================

# ENS160 er ikke implementeret endnu
# Midlertidig test værdi
fEco2 = 0.05


# =====================================================
# CHECK EVENTS
# =====================================================

def C_EVENT_CheckEvents():

    global iSoundState
    global iTempState
    global iHumidityState
    global iEco2State


    bPublish = False


    # =====================================================
    # GET SENSOR VALUES
    # =====================================================

    iSound = C_MIC_GetSoundLevel()

    fTemp, fHumidity = C_AHT21_GetData()


    # =====================================================
    # SOUND STATES
    # =====================================================

    iPreviousSoundState = iSoundState


    # Under 30 dB
    if iSound < 30:

        iSoundState = STATE_SOUND_VERY_LOW


    # 30 dB -> 40 dB
    elif iSound < 40:

        iSoundState = STATE_SOUND_GOOD


    # 40 dB -> 80 dB
    elif iSound < 80:

        iSoundState = STATE_SOUND_HIGH


    # Over 80 dB
    else:

        iSoundState = STATE_SOUND_VERY_HIGH


    # Publish hvis state ændres
    if iSoundState != iPreviousSoundState:

        print("EVENT: SOUND STATE CHANGED")

        print(
            "Old:",
            iPreviousSoundState,
            "New:",
            iSoundState
        )

        bPublish = True


    # =====================================================
    # TEMPERATURE STATES
    # =====================================================

    iPreviousTempState = iTempState


    # Under 17.5°C
    if fTemp < 17.5:

        iTempState = STATE_TEMP_TOO_COLD


    # 17.5°C -> 19.5°C
    elif fTemp < 19.5:

        iTempState = STATE_TEMP_COLD


    # 19.5°C -> 21.5°C
    elif fTemp < 21.5:

        iTempState = STATE_TEMP_GOOD


    # 21.5°C -> 24.5°C
    elif fTemp < 24.5:

        iTempState = STATE_TEMP_GREAT


    # Over 24.5°C
    else:

        iTempState = STATE_TEMP_HOT


    # Publish hvis state ændres
    if iTempState != iPreviousTempState:

        print("EVENT: TEMP STATE CHANGED")

        print(
            "Old:",
            iPreviousTempState,
            "New:",
            iTempState
        )

        bPublish = True


    # =====================================================
    # HUMIDITY STATES
    # =====================================================

    iPreviousHumidityState = iHumidityState


    # Under 40%
    if fHumidity < 40:

        iHumidityState = STATE_HUMIDITY_LOW


    # 40% -> 65%
    elif fHumidity <= 65:

        iHumidityState = STATE_HUMIDITY_GOOD


    # Over 65%
    else:

        iHumidityState = STATE_HUMIDITY_HIGH


    # Publish hvis state ændres
    if iHumidityState != iPreviousHumidityState:

        print("EVENT: HUMIDITY STATE CHANGED")

        print(
            "Old:",
            iPreviousHumidityState,
            "New:",
            iHumidityState
        )

        bPublish = True


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


    return bPublish


# =====================================================
# CREATE PAYLOAD
# =====================================================

def C_EVENT_CreatePayload():

    iSound = C_MIC_GetSoundLevel()

    fTemp, fHumidity = C_AHT21_GetData()


    payload = {

        # Sensor værdier
        "temperature": fTemp,
        "humidity": fHumidity,
        "sound": iSound,
        "eco2": fEco2
    }


    return ujson.dumps(payload)