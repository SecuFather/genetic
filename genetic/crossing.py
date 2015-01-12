from random import randint

def average(x, y, params):
    minx, maxx, resolution = params
    d = maxx-minx
    dx = d/resolution
    avg = (x+y)/2.0-minx
    return int((avg/d)*resolution)*dx + minx

def one_point(x, y, params):
    minx, maxx, resolution = params
    d = maxx-minx
    dd = d/resolution
    dx = x-minx
    dy = y-minx

    xx = int(dx/d*resolution)
    yy = int(dy/d*resolution)

    nbits = len(bin(resolution))-3
    mask = 2**randint(0, nbits)-1
    result = (xx & ~mask) + (yy & mask)
    return minx + result/resolution*dd



table = [average, one_point]
