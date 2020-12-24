#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

if len(sys.argv) == 1:
    sys.argv += ["input_24"]

sample_input=open("input_24_sample").read()

color_black = 1
color_white = 0

def parse_input(lines):
    grid = {}
    moves = {'e': 2, 'ne': 1+1j, 'nw': -1+1j, 'w': -2, 'sw': -1-1j, 'se': 1-1j}
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        p = 0+1j
        line = iter(line)
        for c in line:
            if c == 'n' or c == 's':
                c += next(line)
            p += moves[c]
        grid[p] = 1 - grid.get(p, color_white)
    
    return grid

def work_p1(lines):
    grid = parse_input(lines)
    
    return sum(1 for e in grid.values() if e == color_black)

def work_p2(lines, days=100):
    grid = parse_input(lines)
    
    def adjacents(p):
        return [p+2, p+1+1j, p-1+1j, p-2, p-1-1j, p+1-1j]
    
    def count_black_adjacents(p):
        return sum(1 for pa in adjacents(p) if grid.get(pa, color_white) == color_black)
    
    for day in range(days):
        to_flip = set()
        to_check = set()
        # remove white tiles because I'm lazy
        grid = {p: v for p,v in grid.items() if v == color_black}
        for p, v in grid.items():
            to_check.add(p)
            to_check.update(adjacents(p))
        for p in to_check:
            v = grid.get(p, color_white)
            black_adjacents = count_black_adjacents(p)
            if v == color_black and (black_adjacents == 0 or black_adjacents > 2):
                to_flip.add(p)
            elif v == color_white and black_adjacents == 2:
                to_flip.add(p)
        for p in to_flip:
            grid[p] = 1 - grid.get(p, color_white)
    
    return sum(1 for e in grid.values() if e == color_black)
                

def test_p1():
    assert work_p1(sample_input.splitlines()) == 10
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input.splitlines()) == 2208
test_p2()

def p1():
    print(work_p2(fileinput.input()))
p1()
