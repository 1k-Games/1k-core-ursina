from print_tricks import pt
from ursina import *

def run():
    pt.c('------- tiny_energy_game ---------')
    
if __name__ == "__main__":
    app = Ursina(
    # development_mode=False
    )
    
    run()
    
    app.run()