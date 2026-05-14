
# Configuration
MAX_NUM_OF_TASKS = 10
TM_TIMER_INTERVAL = 1
bPrintDebug = False

# Task storage and indices
listTasks = []
TASK_NAME = 0
TASK_INTERVAL = 1
TASK_TIMER = 2
TASK_CALLBACK = 3

# Create new task with name, interval (ms), and callback function
def C_TM_CreateTask( strTaskName: str, iInterval_ms: int, funcCallback ):

    iNumOfTasks = len(listTasks)
    
    if iNumOfTasks < MAX_NUM_OF_TASKS:
        listTemp = [strTaskName, iInterval_ms, 0, funcCallback]
        listTasks.append(listTemp)

        if bPrintDebug == True:
            print(f"Task number {iNumOfTasks} added succesfully")
       
    else:
        if bPrintDebug == True:
            print("Task not added due to max number of tasks")

# Decrement timers for all tasks (called every 1 ms by IRQ)
def C_TM_Update_ISR():
    i = 0
    for thisTask in listTasks:
        if thisTask[TASK_TIMER] > 0:
            thisTask[TASK_TIMER] -= TM_TIMER_INTERVAL
            listTasks[i] = thisTask
        i += 1
    
# Execute tasks that have timed out and reschedule them
def C_TM_Execute():
    i = 0

    for thisTask in listTasks:
        if thisTask[TASK_TIMER] <= 0:
            thisTask[TASK_TIMER] = thisTask[TASK_INTERVAL]
            listTasks[i] = thisTask

            if( thisTask[TASK_CALLBACK] ):
                thisTask[TASK_CALLBACK]()

            if bPrintDebug == True:
                print( "Task: " + thisTask[TASK_NAME] ) 
        i += 1

