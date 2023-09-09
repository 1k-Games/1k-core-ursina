'''A simple bidict that should give us everything we need. 
For more comprehensive Bi Dict data structures: https://github.com/jab/bidict/blob/main/bidict/_bidict.py 
This is in case we need frozen bi-dicts, orodered bi_dicts, or frozen ordered bi dicts etc. 

    '''
import collections

class BiDict(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)
        self._inverse = {v: k for k, v in self._data.items()}
        
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._inverse[value] = key
        self._data[key] = value
        
    def __delitem__(self, key):
        del self._inverse[self._data[key]]
        del self._data[key]
        
    def pop(self, key, *args):
        if key in self:
            del self[key]
        elif args:
            return args[0]
        else:
            raise KeyError(key)
        
    def popitem(self):
        key, value = self._data.popitem()
        del self._inverse[value]
        return key, value
        
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})"
    
    def get(self, key, default=None, inverse=False):
        if inverse:
            return self._inverse.get(key, default)
        return self._data.get(key, default)
    
    def inverse(self):
        bd = BiDict()
        bd._data = self._inverse
        bd._inverse = self._data
        return bd
    
    def copy(self):
        return self.__class__(self._data.copy())
    
    def clear(self):
        self._data.clear()
        self._inverse.clear()