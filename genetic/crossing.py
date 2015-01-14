from random import randint

def average(population):
    man, woman = population
    return {'x':(man['x'] + woman['x'])/2}

def one_point(population):
    return population

def two_point(population):
    return population

table = [average, one_point, two_point]
