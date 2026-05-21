# MQTT modul til TaskManager
# Håndterer WiFi, MQTT og publishing

import network

from umqtt.simple import MQTTClient

from eventMannager import *


# =========================
# CONFIG
# =========================

MQTT_TASK_INTERVAL_MS = 100

# Heartbeat publish hver 10 min
MQTT_PUBLISH_INTERVAL_MS = 600000


# WiFi credentials
WIFI_SSID = "Asus2"
WIFI_PASSWORD = "NowakogNielsen2528"


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

state  = STATE_WIFI_CONNECT

publish_timer_ms = 0

wifi_connected = False
mqtt_connected = False


# =========================
# INIT
# =========================

def mqtt_init():

    global state

    wlan.active(True)

    state = STATE_WIFI_CONNECT


# =========================
# WIFI CONNECT
# =========================

def start_wifi():

    print("Connecting to WiFi...")

    wlan.connect(
        WIFI_SSID,
        WIFI_PASSWORD
    )


# =========================
# MQTT CONNECT
# =========================

def connect_broker():

    global mqtt_client
    global mqtt_connected


    try:

        mqtt_client = MQTTClient(
            MQTT_CLIENT_ID,
            MQTT_BROKER
        )

        mqtt_client.connect()

        mqtt_connected = True

        print("MQTT connected")


    except Exception as error:

        mqtt_client = None

        mqtt_connected = False

        print("MQTT failed")

        print(error)


# =========================
# PUBLISH
# =========================

def publish():

    global mqtt_client


    if not mqtt_connected:
        return


    payload = create_payload()


    try:

        mqtt_client.publish(
            MQTT_TOPIC,
            payload
        )

        print("MQTT Published:")

        print(payload)


    except Exception as error:

        print("MQTT publish failed")

        print(error)




# =========================
# TASK
# =========================

def mqtt_task():

    global state
    global publish_timer_ms
    global wifi_connected
    global mqtt_connected


    # =========================
    # WIFI CONNECT
    # =========================

    if state == STATE_WIFI_CONNECT:

        start_wifi()

        state = STATE_WIFI_WAIT


    # =========================
    # WIFI WAIT
    # =========================

    elif state == STATE_WIFI_WAIT:

        if wlan.isconnected():

            wifi_connected = True

            print("WiFi connected")

            print(wlan.ifconfig())

            state = STATE_MQTT_CONNECT


    # =========================
    # MQTT CONNECT
    # =========================

    elif state == STATE_MQTT_CONNECT:

        if not mqtt_connected:

            connect_broker()

        if mqtt_connected:

            state = STATE_RUNNING


    # =========================
    # RUNNING
    # =========================

    elif state == STATE_RUNNING:


        # Detect WiFi disconnect
        if wlan.isconnected() == False:

            print("WiFi disconnected")

            wifi_connected = False
            mqtt_connected = False

            state = STATE_WIFI_CONNECT

            return



        # Event publish
        if check_events():

            publish()

        # Periodic publish
        if publish_timer_ms >= MQTT_PUBLISH_INTERVAL_MS:

            publish_timer_ms = 0

            print("Periodic publish")

            publish()

        else:

            publish_timer_ms += MQTT_TASK_INTERVAL_MS