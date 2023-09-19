from print_tricks import pt

from ursina import *

app = Ursina(size=(1920,1080))
from ursina.prefabs.ursfx import ursfx
s = ursfx([(0.0, 1.0), (0.09, 0.5), (0.1, 0.12), (0.5, 0.76), (1.0, 0.0)], volume=0.75, wave='square', pitch=-30, speed=2.9)

for i in range(10):
    s.play()
    # time.sleep(3)
app.run()




