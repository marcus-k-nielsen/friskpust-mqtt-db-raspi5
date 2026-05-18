from machine import Timer
from C_LED import *
from C_TaskManager import *
from C_Microphone import *

# 1 ms timer interrupt callback
def tick(timer):
    C_TM_Update_ISR()

# Setup timer (1000 Hz periodic interrupt)
tim = Timer() # type: ignore
tim.init(freq=1000, mode=Timer.PERIODIC, callback=tick)

# Initialize external modules
C_LED_Init()
C_MIC_Init()
# Start tasks
C_TM_CreateTask( "LED TASK", 100, C_LED_Task )
C_TM_CreateTask( "MIC TASK", MIC_TASK_INTERVAL_MS, C_MIC_Task )
C_TM_CreateTask("DEBUG TASK",500,C_Debug_Task)
# Add more tasks here...

print("Application running...")

# Main loop - TaskManager controls execution
try:
    while True:
        C_TM_Execute()
except KeyboardInterrupt:
    tim.deinit()
    print("Application exit")