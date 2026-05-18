# Maksimalt antal tasks systemet kan håndtere
MAX_NUM_OF_TASKS = 10

# Timer interval i millisekunder
# Bruges af interrupt systemet
TM_TIMER_INTERVAL = 1

# Slår debug print til/fra
bPrintDebug = False


# Liste som indeholder alle oprettede tasks
listTasks = []


# Index værdier til task listen
# Gør koden mere læsbar
TASK_NAME = 0
TASK_INTERVAL = 1
TASK_TIMER = 2
TASK_CALLBACK = 3


# Opretter en ny task
def C_TM_CreateTask(

    strTaskName: str,
    iInterval_ms: int,
    funcCallback
):

    # Finder antal eksisterende tasks
    iNumOfTasks = len(listTasks)


    # Sikrer at der ikke oprettes for mange tasks
    if iNumOfTasks < MAX_NUM_OF_TASKS:


        # Opretter task struktur
        # [navn, interval, timer, callback]
        listTemp = [

            strTaskName,
            iInterval_ms,
            0,
            funcCallback
        ]


        # Tilføjer task til task listen
        listTasks.append(listTemp)


        # Debug print
        if bPrintDebug == True:

            print(
                f"Task number {iNumOfTasks} added succesfully"
            )


    else:

        # Debug print hvis task ikke kunne oprettes
        if bPrintDebug == True:

            print(
                "Task not added due to max number of tasks"
            )


# Opdaterer task timere
# Kaldes hvert millisekund af timer interrupt
def C_TM_Update_ISR():

    i = 0


    # Gennemgår alle tasks
    for thisTask in listTasks:


        # Hvis task timeren er over 0
        # tælles den ned
        if thisTask[TASK_TIMER] > 0:

            thisTask[TASK_TIMER] -= TM_TIMER_INTERVAL

            # Gemmer den opdaterede task tilbage i listen
            listTasks[i] = thisTask


        i += 1


# Kører tasks som er klar
def C_TM_Execute():

    i = 0


    # Gennemgår alle tasks
    for thisTask in listTasks:


        # Hvis task timeren er 0 eller mindre
        # er tasken klar til at blive kørt
        if thisTask[TASK_TIMER] <= 0:


            # Resetter task timeren
            # så tasken kan køres igen senere
            thisTask[TASK_TIMER] = thisTask[TASK_INTERVAL]


            # Gemmer tasken tilbage i listen
            listTasks[i] = thisTask


            # Hvis tasken har en callback funktion
            # køres funktionen
            if(thisTask[TASK_CALLBACK]):

                thisTask[TASK_CALLBACK]()


            # Debug print
            if bPrintDebug == True:

                print(
                    "Task: "
                    + thisTask[TASK_NAME]
                )


        i += 1