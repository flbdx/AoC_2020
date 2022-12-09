#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_12"]

sample_input="""F10
N3
F7
R90
F11"""

cos_table = {0: 1, 90: 0, 180: -1, 270: 0, -90: 0, -180: -1, -270: 0}
sin_table = {0: 0, 90: 1, 180: 0, 270: -1, -90: -1, -180: 0, -270: 1}

class Ship_p1(object):
    def __init__(self):
        self.p = [0, 0]
        self.wp = [1, 0]
    
    def do_F(self, n):
        self.p[0] += self.wp[0] * n
        self.p[1] += self.wp[1] * n
    
    def do_R(self, a):
        self.do_L(-a)
    
    def do_L(self, a):
        cos_theta = cos_table[a]
        sin_theta = sin_table[a]

        nx = self.wp[0] * cos_theta - self.wp[1] * sin_theta
        ny = self.wp[0] * sin_theta + self.wp[1] * cos_theta
        self.wp = [nx, ny]
    
    def do_N(self, n):
        self.p[1] += n
    def do_S(self, n):
        self.p[1] -= n
    def do_E(self, n):
        self.p[0] += n
    def do_W(self, n):
        self.p[0] -= n
    
    def move(self, line):
        i = line[0]
        v = int(line[1:])
        i = getattr(self.__class__, "do_" + i)
        i(self, v)
    
    #def __str__(self):
        #return "[{0}, {1}] : ({2}, {3})".format(self.p[0], self.p[1], self.wp[0], self.wp[1])
    
    def manhattan(self):
        return abs(self.p[0]) + abs(self.p[1])

class Ship_p2(Ship_p1):
    def __init__(self):
        super().__init__()
        self.wp = [10, 1]
    
    def do_N(self, n):
        self.wp[1] += n
    def do_S(self, n):
        self.wp[1] -= n
    def do_E(self, n):
        self.wp[0] += n
    def do_W(self, n):
        self.wp[0] -= n

def work_p1(lines):
    ship = Ship_p1()
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        ship.move(line)
    return ship.manhattan()

def work_p2(lines):
    ship = Ship_p2()
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        ship.move(line)
    return ship.manhattan()

def test_p1():
    assert work_p1(sample_input.splitlines()) == 25
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input.splitlines()) == 286
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
