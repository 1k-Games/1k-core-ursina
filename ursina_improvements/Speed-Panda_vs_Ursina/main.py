from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)

import os
import subprocess

os.environ["TIME_BETWEEN_PRINTS"] = "5"
os.environ["TOT_TIME_TO_RUN"] = "10"

run_same_time = True 
run_same_time = False 

if run_same_time:
    ursina_process = subprocess.Popen(["python", fr"ursina_improvements/Speed-Panda_vs_Ursina/ursina_speed.py"])
    panda_process = subprocess.Popen(["python", fr"ursina_improvements/Speed-Panda_vs_Ursina/panda_speed.py"])
    ursina_process.wait()
    panda_process.wait()
else:
    subprocess.run(["python", fr"ursina_improvements/Speed-Panda_vs_Ursina/ursina_speed.py"])
    subprocess.run(["python", fr"ursina_improvements/Speed-Panda_vs_Ursina/panda_speed.py"])

'''

'''