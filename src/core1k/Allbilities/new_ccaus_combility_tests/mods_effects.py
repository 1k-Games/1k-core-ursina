from print_tricks import pt

from mod_category_one import *
from mod_category_two import *


if __name__ == "__main__":
    class blah:
        
        mod_one_a = mod_one_a
        # m1a = mod_one_a
        # mod_one_a('custom arg')
        # mod_one_a('custom arg', 'custom kwarg')
    blah().mod_one_a()


    mod_two_instance = Mod_Category_Two()
    mod_two_a = mod_two_instance.mod_two_a
    mod_two_b = mod_two_instance.mod_two_b

    mod_two_a()
    mod_two_a('2a custom kwarg')

    mod_two_b('2b custom arg')
    mod_two_b('2b custom arg', '2b custom kwarg')
