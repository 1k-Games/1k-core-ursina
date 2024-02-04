from print_tricks import pt


class Mod_One_A:
    def random_function_needed_for_mod_one_a(self):
        pt(self.random_function_needed_for_mod_one_a.__name__)
        
    def prepare_mod_one_a(self, a, b='mod_one_a default kwarg'):
        pt(a)
    
    def use_mod_one_a(self, b='optional kwarg'):
        pt(b)
        
class Mod_One_B:
    def use_mod_one_b(self, b, c='mod_one_b default kwarg'):
        pt(b, c)
    
    def update_mod_one_b(self):
        pt('inside the update')