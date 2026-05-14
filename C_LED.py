# A simple module to demonstrate a module used by the TaskManager.
# It simple implements Init() and a Task() functions.
# The task simply toggle the Pico LED
# This file can be used as a template when you start
# developing new modules.

from machine import Pin

# Hardware config
ledPico = Pin("LED", Pin.OUT)
LED_TASK_INTERVAL_MS = 100

# Local variables
iToggleTimer_ms = 0

# Initialize LED (must be called at power up)
def C_LED_Init():
    pass

# Toggle LED every 500 ms (called every LED_TASK_INTERVAL_MS)
def C_LED_Task():
    global iToggleTimer_ms

    if iToggleTimer_ms >= 500:
        ledPico.toggle()
        iToggleTimer_ms = 0

    iToggleTimer_ms += LED_TASK_INTERVAL_MS

