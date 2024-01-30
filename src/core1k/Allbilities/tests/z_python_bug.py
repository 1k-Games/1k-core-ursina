

string = 'pt(hello)'
string = 'pt(self.player.hand_r.world_position,'
# newstr = string.replace('(', '')
newstr = string.replace('(','').replace(')', '').replace('dpt', '').replace('pts', '').replace('pt', '')

print(newstr)