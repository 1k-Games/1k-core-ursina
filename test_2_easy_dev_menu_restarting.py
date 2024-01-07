from src.core1k.controllers.controls_center import ControlsCenter
from ursina import *
from print_tricks import pt 
pt.easy_testing(__name__)

Entity(model='sphere', x=4)
def run():
    cc = ControlsCenter(incoming_name=__name__, incoming_filename=__file__)
    
if __name__ == '__main__':
    app=Ursina()
    run()
    app.run()