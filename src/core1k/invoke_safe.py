from ursina import *

def invoke_safe(function, *args, **kwargs):
    try:
        delay = 0
        if 'delay' in kwargs:
            delay = kwargs['delay']
            del kwargs['delay']

        if not delay:
            function(*args, **kwargs)
            return function

        s = Sequence(
            Wait(delay),
            Func(function, *args, **kwargs)
        )
        s.start()
        return s
    except Exception as ex:
        print(f"Error in invoke_safe: {type(ex).__name__}, {ex.args}")