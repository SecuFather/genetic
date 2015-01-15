import random

def average(couple, pop_size):
    man, woman = couple
    return {'x': (man['x'] + woman['x'])/2}

def one_point(couple, pop_size):
    man, woman = couple
    g_point = random.randrange(pop_size)
    wmask = 2**g_point-1
    mmask = 2**pop_size-1-wmask

    return {'x': (mmask & man['x']) | (wmask & woman['x'])}

def two_point(couple, pop_size):
    return couple

table = [average, one_point, two_point]
