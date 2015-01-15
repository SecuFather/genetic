import random

def negation(beast, pop_size):
    return 2**pop_size-1-beast

def defect(beast, pop_size):
    return 2**random.randrange(pop_size) ^ beast

def swap(beast, pop_size):
    a = random.randrange(1, pop_size)
    b = random.randrange(a)

    ax = (2**b & beast) << (a-b)
    bx = (2**a & beast) >> (a-b)

    return beast & ax & bx