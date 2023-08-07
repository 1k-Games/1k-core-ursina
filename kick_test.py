from ursina import *
from src.core1k.stream_manager.kick import Kick

from datetime import datetime, timezone
from dateutil.parser import isoparse

class KickManager(Entity):
    def __init__(self, kick, **kwargs):
        super().__init__(**kwargs)

        self.kick = kick
        self.kick.channel()

        self.players = []

        self.check = True
        
        self.last_check = datetime.utcnow()
        self.last_check = self.last_check.replace(tzinfo=timezone.utc)
        
        self.check_every = 10
        self.check_timer = 0

    def update(self):
        self.check_timer += time.dt

        if self.check_timer >= self.check_every:
            for message in self.kick.messages():
                message_created = isoparse(message['created_at'])
                message_created.replace(tzinfo=timezone.utc)

                if message_created > self.last_check:
                    if message['content'].startswith('!join') and not message['sender']['username'] in self.players:
                        self.add_player(message['sender']['username'])

            self.check_timer = 0
            self.last_check = datetime.utcnow()
            self.last_check = self.last_check.replace(tzinfo=timezone.utc)

    def add_player(self, name):
        self.players.append(name)
        
        c = color.rgb(random.randint(0, 225), random.randint(0, 225), random.randint(0, 225))
        x = random.randint(-5, 5)

        new_player = Entity(model='sphere', color=c, x=x, y=0)
        Text(parent=new_player, text=name, scale_x=1, scale_y=1, y=2)


app = Ursina( 
    size=(1200,800), 
    vsync=False
)

kick = Kick('konvay')
KickManager(kick)

app.run()