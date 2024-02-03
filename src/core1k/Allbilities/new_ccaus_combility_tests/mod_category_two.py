from print_tricks import pt

class Mod_Two_A:
    def prepare_mod_two_a(self, d='mod_two_a default kwarg'):
        pt(d)

    def update_mod_two_a(self, d):
        pt(d)
        
    def use_mod_two_a(self):
        pt('inside of use_mod_two_a')
class Mod_Two_B:
    def prepare_mod_two_a(self, e, f='hello'):
        pt('prep mod two b')
        
    def update_mod_two_a(self):
        pt('inside mod two b update, with no args/kwargs')
        
    def enable_mod_two_b(self, e, f='mod_two_b default kwarg'):
        pt(e, f)
        
    def disable_mod_two_b(self, e, f):
        pt(e, f)
