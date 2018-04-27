"""
generate hash function
"""

from geo.point import Point
from geo.quadrant import Quadrant
from geo.segment import Segment
from math import ceil
from itertools import combinations

def h1(p , t):
    return (ceil(p.coordinates[0]/t) , ceil(p.coordinates[1]/t))
def h2(p , t):
    return (ceil(p.coordinates[0]/t+1/2) , ceil(p.coordinates[1]/t))
def h3(p , t):
    return (ceil(p.coordinates[0]/t) , ceil(p.coordinates[1]/t+1/2))
def h4(p , t):
    return (ceil(p.coordinates[0]/t+1/2) , ceil(p.coordinates[1]/t+1/2))

def hasher(points , t):
    D1 , D2 , D3 , D4 = dict() , dict() , dict() , dict()
    for point in points:
        if h1(point) not in D1:
            D1[h1(point)] = []
        D1[h1(point)].append(point)
        if h2(point) not in D2:
            D2[h2(point)] = []
        D2[h2(point)].append(point)
        if h3(point) not in D3:
            D3[h3(point)] = []
        D3[h3(point)].append(point)
        if h4(point) not in D4:
            D4[h4(point)] = []
        D4[h4(point)].append(point)
    return (D1,D2,D3,D4)

def collision(jeu):
    for dic in jeu:
        for key in dic.keys():
            if len(dic[key])!=1:
                return True
    return False

def ordered_segments(points,t0=10):
    t = t0
    tables = [hasher(points , t)]
    while collision(tables[-1]):
        t /=2
        tables.append(hasher(points,t))
    for jeu in tables.reverse():
        for table in jeu:
            for key in table.keys():
                for couple in combinations(table[key],2):
                    yield Segment(list(couple))

