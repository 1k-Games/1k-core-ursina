from print_tricks import pt
from ursina import *

def run():
    pt.c('------- companion ---------')
    
if __name__ == "__main__":
    app = Ursina(
        title='Companion',
        borderless = False,
        fullscreen = False,
    # development_mode=False
    )
    window.cog_button.enabled = False,
    window.exit_button.enabled = False,
    
    run()
    
    app.run()