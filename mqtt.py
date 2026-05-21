# MQTT modul til TaskManager
# Håndterer WiFi, MQTT og publishing

import network

from umqtt.simple import MQTTClient

from C_EventManager import *


# =========================
# CONFIG
# =========================

MQTT_TASK_INTERVAL_MS = 100

# Heartbeat publish hver 10 min
MQTT_PUBLISH_INTERVAL_MS = 600000


# WiFi credentials
WIFI_SSID = "Asus2"
WIFI_PASSWORD = "YOUR_PASSWORD"


# MQTT broker config
MQTT_BROKER = "192.168.50.115"
MQTT_CLIENT_ID = "FriskPust01"

# MQTT topic
MQTT_TOPIC = b"friskpust/classroom01"


# =========================
# STATES
# =========================

STATE_WIFI_CONNECT = 0
STATE_WIFI_WAIT = 1
STATE_MQTT_CONNECT = 2
STATE_RUNNING = 3


# =========================
# VARIABLES
# =========================

wlan = network.WLAN(network.STA_IF)

mqttClient = None

iState = STATE_WIFI_CONNECT

iPublishTimer_ms = 0

bWifiConnected = False
bMqttConnected = False


# =========================
# INIT
# =========================

def mqtt_init():

    global iState

    wlan.active(True)

    iState = STATE_WIFI_CONNECT


# =========================
# WIFI CONNECT
# =========================

def C_MQTT_StartWiFi():

    print("Connecting to WiFi...")

    wlan.connect(
        WIFI_SSID,
        WIFI_PASSWORD
    )


# =========================
# MQTT CONNECT
# =========================

def C_MQTT_ConnectBroker():

    global mqttClient
    global bMqttConnected

    try:

        mqttClient = MQTTClient(
            MQTT_CLIENT_ID,
            MQTT_BROKER
        )

        mqttClient.connect()

        bMqttConnected = True

        print("MQTT connected")

    except Exception as e:

        mqttClient = None

        bMqttConnected = False

        print("MQTT failed")
        print(e)


# =========================
# PUBLISH
# =========================

def C_MQTT_Publish():

    global mqttClient

    if bMqttConnected == False:
        return


    payload = C_EVENT_CreatePayload()


    try:

        mqttClient.publish(
            MQTT_TOPIC,
            payload
        )

        print("MQTT Published:")
        print(payload)

    except Exception as e:

        print("MQTT publish failed")
        print(e)


# =========================
# TASK
# =========================

def C_MQTT_Task():

    global iState
    global iPublishTimer_ms
    global bWifiConnected
    global bMqttConnected


    # =========================
    # WIFI CONNECT
    # =========================

    if iState == STATE_WIFI_CONNECT:

        C_MQTT_StartWiFi()

        iState = STATE_WIFI_WAIT


    # =========================
    # WIFI WAIT
    # =========================

    elif iState == STATE_WIFI_WAIT:

        if wlan.isconnected():

            bWifiConnected = True

            print("WiFi connected")
            print(wlan.ifconfig())

            iState = STATE_MQTT_CONNECT


    # =========================
    # MQTT CONNECT
    # =========================

    elif iState == STATE_MQTT_CONNECT:

        if bMqttConnected == False:

            C_MQTT_ConnectBroker()

        if bMqttConnected:

            iState = STATE_RUNNING


    # =========================
    # RUNNING
    # =========================

    elif iState == STATE_RUNNING:


        # Detect WiFi disconnect
        if wlan.isconnected() == False:

            print("WiFi disconnected")

            bWifiConnected = False
            bMqttConnected = False

            iState = STATE_WIFI_CONNECT

            return


        # Event publish
        if C_EVENT_CheckEvents():

            C_MQTT_Publish()


        # Periodic publish
        if iPublishTimer_ms >= MQTT_PUBLISH_INTERVAL_MS:

            iPublishTimer_ms = 0

            print("Periodic publish")

            C_MQTT_Publish()

        else:

            iPublishTimer_ms += MQTT_TASK_INTERVAL_MS