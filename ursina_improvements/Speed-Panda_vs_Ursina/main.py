'''
dad_pc: 
    82%: 
        OFF dev_mode
            8254 fps ursina
            10112 fps panda
    16%
        ON dev_mode
            1632 fps ursina
            10152 fps panda
'''
from print_tricks import pt
# pt.easy_imports()
# pt.easy_testing(__name__)
import os
import subprocess

run_apps_at_the_same_time = True 
# run_apps_at_the_same_time = False

os.environ["TIME_BETWEEN_PRINTS"] = "5"
os.environ["TOT_TIME_TO_RUN"] = "15"

dad_pc = 'c:/.PythonProjects/sg/1k-core-ursina'

ursina_file = dad_pc + '/ursina_improvements/Speed-Panda_vs_Ursina/ursina_speed.py'
panda_file = dad_pc + '/ursina_improvements/Speed-Panda_vs_Ursina/panda_speed.py'



if run_apps_at_the_same_time:
    ursina_process = subprocess.Popen(["python", ursina_file])
    panda_process = subprocess.Popen(["python", panda_file])
    ursina_process.wait()
    panda_process.wait()
else:
    subprocess.run(["python", ursina_file])
    subprocess.run(["python", panda_file])

'''




'''