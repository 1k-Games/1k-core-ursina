import importlib
import inspect

from mods_all_mods_easy_access import *

class Mods:
    def __init__(self, *mod_methods):
        self.mods_info = {}
        for method in mod_methods:
            method_name = method.__name__
            mod_data = {
                'method': method,          # Store the function itself for later use
                'position': None,          # Placeholder for actual position
                'rotation': None,          # Placeholder for actual rotation
                'size': .025,              # Placeholder for actual size
                'model_info': {
                    'vertices': None,       # Placeholder for actual vertices
                    'triangles': None,      # Placeholder for actual triangles
                    'normals': None,        # Placeholder for actual normals
                    'uvs': None             # Placeholder for actual uvs
                },
                'texture': None            # Placeholder for actual texture
            }
            self.mods_info[method_name] = mod_data

    def print_mod_source(self, mod_method):
        try:
            source_code = inspect.getsource(mod_method)
            print(source_code)
        except TypeError:
            print(f"The source code for {mod_method.__name__} could not be found.")

    def print_all_mod_sources(self):
        # Access the global namespace to find the imported methods.
        global_namespace = globals()
        for method_name, mod_data in self.mods_info.items():
            # Check if the method_name exists in the global namespace
            mod_method = global_namespace.get(method_name, None)
            if not mod_method:
                # If the method is not found, it might be a class method.
                # Attempt to find the class in the global namespace and then the method.
                for global_name, global_value in global_namespace.items():
                    if inspect.isclass(global_value):
                        mod_method = getattr(global_value, method_name, None)
                        if mod_method:
                            break
            
            if mod_method:
                try:
                    source_code = inspect.getsource(mod_method)
                    print(f"Source code for {method_name}:\n{source_code}\n")
                except TypeError:
                    print(f"The source code for {method_name} could not be found.")
            else:
                print(f"Method {method_name} not found in the global namespace or as a class method.")




if __name__ == "__main__":
    mod_mix_1 = Mods(mod_one_a, Mod_Category_Two.mod_two_a)
    mod_mix_2 = Mods(Mod_Category_Two.mod_two_b, Mod_Category_Two.mod_two_a, mod_one_b)

    pt(mod_mix_1.mods_info)
    pt(mod_mix_2.mods_info)
    # mod_mix_1.print_mod_source(mod_one_a)
    # mod_mix_1.print_mod_source(Mod_Category_Two.mod_two_a)

    # mod_mix_1.print_all_mod_sources()
    # mod_mix_2.print_all_mod_sources()