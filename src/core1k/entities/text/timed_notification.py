from ursina import *
from enum import Enum

# TODO: Make positioning easy
# TODO: Make scaling easy
class TimedNotification(Entity):
    def __init__(self, text, icon=None, display_time=3, scrolling=True, scroll_speed=2, **kwargs):
        super().__init__(**kwargs)
        self.parent=camera.ui
        
        self.has_icon = icon != None
        if self.has_icon: 
            self.notification_icon = Entity(parent=self.notification_text, x=-0.05, y=-0.015, model='quad', texture=icon, scale=(0.05, 0.05))
        
        self.notification_text = Text(parent=self, x=-0.65, y=-0.25, text=text)


        self.display_time = display_time
        self.scroll_speed = scroll_speed
        self.alpha = 1

    def update(self):
        self.display_time -= time.dt
        self.notification_text.y += time.dt * .1
        
        self.alpha -= time.dt * 1 / self.display_time
        self.notification_text.alpha = self.alpha

        if self.has_icon:
            self.notification_icon.alpha = self.alpha

        if self.display_time <= 0:
            destroy(self)

if __name__ == '__main__':
    app=Ursina(size=(1200, 800), fullscreen=False)
    TimedNotification('Hello', None, 3, True, 5)
    app.run()