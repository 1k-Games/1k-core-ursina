import importlib
import time
import types
import threading
import pathlib

TO_HOT_RELOAD = set()
LAST_MODIFIED = {}


def file_watcher():
    while True:
        for module in TO_HOT_RELOAD.copy():
            file = pathlib.Path(module.__file__)
            if file.stat().st_mtime > LAST_MODIFIED[module]:
                print(f"Reloading {file}")
                LAST_MODIFIED[module] = file.stat().st_mtime
                importlib.reload(module)
        time.sleep(1)

def import_deco(old_import_f):
    def wrapped(name, globals=None, locals=None, fromlist=(), level=0):
        m = old_import_f(name, globals, locals, fromlist, level)
        if isinstance(m, types.ModuleType):
            try:
                if hasattr(m, '__file__') and m.__file__ is not None:
                    file = pathlib.Path(m.__file__)
                    if file.suffix == ".py" and m not in TO_HOT_RELOAD:
                        TO_HOT_RELOAD.add(m)
                        LAST_MODIFIED[m] = file.stat().st_mtime
                        print(f"Added {file} to hot reload list")
            except AttributeError:
                pass
        return m
    return wrapped

__builtins__["__import__"] = import_deco(__builtins__["__import__"])

threading.Thread(target=file_watcher, daemon=True).start()
