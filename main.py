from machine import Timer
from C_LED import *
from C_TaskManager import *
from C_Microphone import *

#############################################################
# Import external modules
#############################################################
from C_TaskManager import *
from C_AHT21 import *

#############################################################
# Module setup
#############################################################

#############################################################
# Hardware config
#############################################################
# 1 ms timer interrupt:
# Define the IRQ callback ISR:
def tick(timer):
    C_TM_Update_ISR()

# Setup timer interrupt:
# It is necessary to ignore a warning, because the interpreter 
# expects an argument for the Timer() function.
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
#############################################################
# Local variables
#############################################################

#############################################################
# Init external modules
#############################################################
C_AHT21_Init()

#############################################################
# Private functions
#############################################################
    
#############################################################
# Start tasks
#############################################################
C_TM_CreateTask( "AHT21 TASK", 100, C_AHT21_Task )


###################################################################################################
# Application is now ready to fly...
###################################################################################################
print("Application running...")

# Main loop: Simply calls the TM as fast as possible
# TM is now in control of the system.
try:
    while True:
        C_TM_Execute()
except KeyboardInterrupt:
    tim.deinit()
    print( "Application exit")
finally:
    # Clean up before exit
    pass