from print_tricks import pt

class Mod_Two_A:
    def update_mod_two_a(self, d='another optional kwarg'):
        pt(d)
        
    def use_mod_two_a(self):
        pt('inside of use_mod_two_a')
class Mod_Two_B:
    def prepare_mod_two_b(self, e, f='hello'):
        pt('prep mod two b')
        
    def update_mod_two_b(self):
        pt('inside mod two b update, with no args/kwargs')
        
    def enable_mod_two_b(self, f='mod_two_b default kwarg'):
        pt(f)
        
    def disable_mod_two_b(self):
        pt('disable mod two b')
        
    def extra_helper_function(self):
        pt('extra helper function')
