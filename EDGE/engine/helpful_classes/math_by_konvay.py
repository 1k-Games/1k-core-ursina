import math
import numpy

def floor_to_zero(num, denum):
    if(num * denum > 0):
        return num // denum
    else :
        return math.ceil(num / denum)
    
print(floor_to_zero(-5, 2))
print(floor_to_zero(5, 2))

print(numpy.floor(-5/2))