from print_tricks import pt
pt.easy_imports()

from panda3d.core import NodePath, loadPrcFileData
from direct.showbase.ShowBase import ShowBase

from ursina import *


class Test_Aura_Python:
    def __init__(self, arg1, arg2, arg3, arg4, arg5, **kwargs):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        self.arg5 = arg5
        self.arg6 = kwargs.get('arg6', None)
        self.arg7 = kwargs.get('arg7', None)
        self.arg8 = kwargs.get('arg8', None)
        self.arg9 = kwargs.get('arg9', None)
        self.arg10 = kwargs.get('arg10', None)

    def func1(self): print("Function 1")
    def func2(self): print("Function 2")
    def func3(self): print("Function 3")
    def func4(self): print("Function 4")
    def func5(self): print("Function 5")
    def func6(self): print("Function 6")
    def func7(self): print("Function 7")
    def func8(self): print("Function 8")
    def func9(self): print("Function 9")
    def func10(self): print("Function 10")
    def func11(self): print("Function 11")
    def func12(self): print("Function 12")
    def func13(self): print("Function 13")
    def func14(self): print("Function 14")
    def func15(self): print("Function 15")

class Test_Aura_NodePath(NodePath):
    def __init__(self, arg1, arg2, arg3, arg4, arg5, 
                    parent = scene, 
                    **kwargs):
        super().__init__(self.__class__.__name__)
        if parent is not None:
            self.reparentTo(parent)
            
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        self.arg5 = arg5
        self.arg6 = kwargs.get('arg6', None)
        self.arg7 = kwargs.get('arg7', None)
        self.arg8 = kwargs.get('arg8', None)
        self.arg9 = kwargs.get('arg9', None)
        self.arg10 = kwargs.get('arg10', None)

    def func1(self): print("Function 1")
    def func2(self): print("Function 2")
    def func3(self): print("Function 3")
    def func4(self): print("Function 4")
    def func5(self): print("Function 5")
    def func6(self): print("Function 6")
    def func7(self): print("Function 7")
    def func8(self): print("Function 8")
    def func9(self): print("Function 9")
    def func10(self): print("Function 10")
    def func11(self): print("Function 11")
    def func12(self): print("Function 12")
    def func13(self): print("Function 13")
    def func14(self): print("Function 14")
    def func15(self): print("Function 15")

class Test_Aura_Entity(Entity):
    def __init__(self, arg1, arg2, arg3, arg4, arg5, parent = scene, **kwargs):
        super().__init__(self.__class__.__name__)
        self.parent = parent
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        self.arg5 = arg5
        self.arg6 = kwargs.get('arg6', None)
        self.arg7 = kwargs.get('arg7', None)
        self.arg8 = kwargs.get('arg8', None)
        self.arg9 = kwargs.get('arg9', None)
        self.arg10 = kwargs.get('arg10', None)

    def func1(self): print("Function 1")
    def func2(self): print("Function 2")
    def func3(self): print("Function 3")
    def func4(self): print("Function 4")
    def func5(self): print("Function 5")
    def func6(self): print("Function 6")
    def func7(self): print("Function 7")
    def func8(self): print("Function 8")
    def func9(self): print("Function 9")
    def func10(self): print("Function 10")
    def func11(self): print("Function 11")
    def func12(self): print("Function 12")
    def func13(self): print("Function 13")
    def func14(self): print("Function 14")
    def func15(self): print("Function 15")



def create_instances(number, class_type, use_dict=False, *args, **kwargs):
    if use_dict:
        instances = {}
        for i in range(number):
            instance = class_type(1, 2, 3, 4, 5, arg6=6, arg7=7, arg8=8, arg9=9, arg10=10, *args, **kwargs)
            instances[f'instance_{i}'] = instance
    else:
        instances = []
        for _ in range(number):
            instance = class_type(1, 2, 3, 4, 5, arg6=6, arg7=7, arg8=8, arg9=9, arg10=10, *args, **kwargs)
            instances.append(instance)
    return instances

def profile_resources(num_instances, class_type):
    import psutil, GPUtil

    process = psutil.Process()
    memory_info = process.memory_info()
    total_system_memory = psutil.virtual_memory().total
    cpu_percent = psutil.cpu_percent(interval=1)

    print(  f"Created {num_instances:,} instances of {class_type.__name__}.\n"
            f"Memory used by the process: {memory_info.rss / (1024 * 1024):.2f} MB / "
            f"{total_system_memory / (1024 * 1024 * 1024):.2f} GB - "
            f"{memory_info.rss / total_system_memory * 100:.2f}% of Total system memory "
            f"({memory_info.rss / num_instances:.0f} bytes per instance)\n"
            f"CPU usage: {cpu_percent}%")

    # GPU usage
    gpus = GPUtil.getGPUs()
    if gpus:
        for gpu in gpus:
            print(  f"GPU {gpu.id}: {gpu.name}, Load: {gpu.load*100:.1f}%, "
                    f"Free Memory: {gpu.memoryFree:.0f}MB, Used Memory: {gpu.memoryUsed:.0f}MB, "
                    f"Total Memory: {gpu.memoryTotal:.0f}MB")
    else:
        print("No GPU found.")
# def profile_memory(num_instances):
#     import psutil

#     # Get the memory usage of the current process
#     process = psutil.Process()
#     memory_info = process.memory_info()
#     total_system_memory = psutil.virtual_memory().total

#     print(  f"Memory used by the process: "
#             f"{memory_info.rss / (1024 * 1024):.2f} MB / {total_system_memory / (1024 * 1024 * 1024):.2f}"
#             f"GB - {memory_info.rss / total_system_memory * 100:.2f}% of Total system memory "
#             f"({memory_info.rss / num_instances:.0f} bytes per instance)")

if __name__ == "__main__":
    
    def test_aura_python(num_instances, use_dict = False):
        pt.t()
        instances = create_instances(num_instances, Test_Aura_Python, use_dict)
        pt.t()
        
        profile_resources(num_instances, Test_Aura_Python)

    def test_aura_nodepaths(num_instances, use_dict = False, parent=scene):
        pt.t()
        instances = create_instances(num_instances, Test_Aura_NodePath, use_dict, parent=parent)
        pt.t()
        
        profile_resources(num_instances, Test_Aura_NodePath)

    def test_aura_entities(num_instances, use_dict = False, add_to_scene_entities = False):
        pt.t()
        instances = create_instances(num_instances, Test_Aura_Entity, use_dict, add_to_scene_entities)
        pt.t()
        
        profile_resources(num_instances, Test_Aura_Entity)
    
    engine = 'panda3d'
    engine = 'ursina'
    
    if engine == 'ursina':
        loadPrcFileData('', '''frame-rate-meter-milliseconds #t
                        ''')
        app = Ursina(development_mode=False)
        app.setFrameRateMeter(True)
        window.fullscreen = False 
        window.size = (1280, 720)


    else:
        class PandaApp(ShowBase):
            def __init__(self):
                super().__init__()
                self.setFrameRateMeter(True)
                
                # props = WindowProperties()
                # props.setFullscreen(True)
                # self.win.requestProperties(props)
    
        app = PandaApp()


    use_dict = False
    
    # test_aura_python(10_000_000, use_dict)
    
    '''NOTE: Nodepaths:
            Parent=Scene:
            - ursina will have a max nodepaths around 200k.
            - panda3d has no known limit (tested millions with high 3k standard panda fps)

            Parent=None:
            - ursina no limit? (1 million was 2k fps)
            
            '''
            
    # test_aura_nodepaths(1_000_000, use_dict, parent=scene)
    # test_aura_nodepaths(1_000_000, use_dict, parent=None)
    test_aura_nodepaths(1_000, use_dict, parent=None)
    
    
    # test_aura_entities(10_000, use_dict, add_to_scene_entities = False)
    # test_aura_entities(10_000, use_dict, add_to_scene_entities = True)
    
    app.run()

