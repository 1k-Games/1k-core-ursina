
import os

def terminate(ProcessName):
    os.system('taskkill /im ' + ProcessName)

terminate('pstats.exe')