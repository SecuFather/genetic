import random

def average(couple, pop_size):
    man, woman = couple
    return {'x': (man['x'] + woman['x'])/2}

def _mask_couple(man, woman, mmask, wmask):
    return {'x': (mmask & man['x']) | (wmask & woman['x'])}

def one_point(couple, pop_size):
    man, woman = couple
    g_point = random.randrange(pop_size)
    wmask = 2**g_point-1
    mmask = 2**pop_size-1-wmask

    return _mask_couple(man, woman, mmask, wmask)

def two_point(couple, pop_size):
    man, woman = couple
    gp1 = random.randrange(1, pop_size)
    gp2 = random.randrange(gp1)

    wmask = 2**gp1-2**gp2
    mmask = 2**pop_size-1-wmask

    return _mask_couple(man, woman, mmask, wmask)

table = [average, one_point, two_point]
