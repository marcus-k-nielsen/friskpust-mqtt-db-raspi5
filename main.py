from machine import Timer

# Importerer TaskManager og moduler
from C_TaskManager import *
from C_Microphone import *
from C_AHT21 import *


# Timer interrupt callback
# Denne funktion køres hvert millisekund
# og opdaterer alle task timere
def tick(timer):

    C_TM_Update_ISR()


# Opretter hardware timer
tim = Timer()  

# Starter periodisk timer interrupt
# freq=1000 betyder:
# 1000 Hz = 1 ms interval
tim.init(

    # Timer frekvens
    freq=1000,

    # Periodisk betyder at timeren kører konstant
    mode=Timer.PERIODIC,

    # Funktion som køres ved hvert interrupt
    callback=tick
)


# Initialiserer moduler
C_MIC_Init()
C_AHT21_Init()


# Registrerer mikrofon task i TaskManageren
C_TM_CreateTask(

    # Task navn
    "MIC TASK",

    # Hvor ofte tasken skal køres
    MIC_TASK_INTERVAL_MS,

    # Funktion som skal køres
    C_MIC_Task
)


# Debug task som printer lydniveau
C_TM_CreateTask(

    "DEBUG TASK",

    # Kører hver 500 ms
    500,

    C_Debug_Task
)


# Temperatur og luftfugtighed task
C_TM_CreateTask(

    "AHT21 TASK",

    # Kører hver 100 ms
    100,

    C_AHT21_Task
)


print("Application running...")


# Main loop
# TaskManageren styrer nu systemet
try:

    while True:

        # Kører tasks som er klar
        C_TM_Execute()


# Stopper programmet sikkert ved CTRL+C
except KeyboardInterrupt:


    # Stopper hardware timeren
    tim.deinit()


    print("Application exit")