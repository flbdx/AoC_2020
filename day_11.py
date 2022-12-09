#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

sample_input="""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

def parse_input(lines):
    grid = {}
    for y, line in enumerate(lines):
        line = line.strip()
        if len(line) == 0:
            continue
        for x, c in enumerate(line):
            grid[x,y] = c
    return grid

def work_p1(lines):
    grid = parse_input(lines)
    
    def adjacents(p):
        return [(p[0]-1, p[1]-1),(p[0]+0, p[1]-1),(p[0]+1, p[1]-1),
                (p[0]-1, p[1]+0),                 (p[0]+1, p[1]+0),
                (p[0]-1, p[1]+1),(p[0]+0, p[1]+1),(p[0]+1, p[1]+1)]
    
    while True:
        ngrid = {}
        no_change = True
        for p, v in grid.items():
            if v == '.':
                ngrid[p] = v
            elif v == 'L':
                n_occupied = sum(1 for pa in adjacents(p) if grid.get(pa, '.') == '#')
                ngrid[p] = '#' if n_occupied == 0 else 'L'
            elif v == '#':
                n_occupied = sum(1 for pa in adjacents(p) if grid.get(pa, '.') == '#')
                ngrid[p] = 'L' if n_occupied >= 4 else '#'
            no_change &= (ngrid[p] == grid[p])
        if no_change:
            break
        grid = ngrid
    
    return sum(1 for v in grid.values() if v == '#')

def work_p2(lines):
    grid = parse_input(lines)
    xmax = max(p[0] for p in grid.keys())
    ymax = max(p[1] for p in grid.keys())
    
    def first_visible(p, direction):
        nonlocal grid, xmax, ymax
        while True:
            p = (p[0] + direction[0], p[1] + direction[1])
            if p[0] < 0 or p[0] > xmax or p[1] < 0 or p[1] > ymax:
                return '.'
            v = grid[p]
            if v != '.':
                return v
    
    directions = [(-1, -1),( 0, -1),(+1, -1),
                  (-1,  0),         (+1,  0),
                  (-1, +1),( 0, +1),(+1, +1)]
    def visibles(p):
        nonlocal directions
        return sum(1 for d in directions if first_visible(p, d) == '#')
    
    while True:
        ngrid = {}
        no_change = True
        for p, v in grid.items():
            if v == '.':
                ngrid[p] = v
            elif v == 'L':
                ngrid[p] = '#' if visibles(p) == 0 else 'L'
            elif v == '#':
                ngrid[p] = 'L' if visibles(p) >= 5 else '#'
            no_change &= (ngrid[p] == grid[p])
        if no_change:
            break
        grid = ngrid

    return sum(1 for v in grid.values() if v == '#')

def test_p1():
    assert(work_p1(sample_input.splitlines()) == 37)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(sample_input.splitlines()) == 26)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
