#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

if len(sys.argv) == 1:
    sys.argv += ["input_17"]

sample_input=""".#.
..#
###"""

def work_p2(lines, n_dims=3, cycles=6):
    grid=set()
    
    for y, line in enumerate(lines):
        line = line.strip()
        if len(line) == 0:
            continue
        for x, c in enumerate(line):
            if c == '#':
                v = [0] * n_dims
                v[0] = x
                v[1] = y
                grid.add(tuple(v))
        
    min_coords = [0] * n_dims
    max_coords = [0] * n_dims
    for c in grid:
        for d in range(n_dims):
            min_coords[d] = min(c[d], min_coords[d])
            max_coords[d] = max(c[d], max_coords[d])
    
    def n_active_neighboors(c):
        nonlocal grid, n_dims
        n_actives = 0
        dim_ranges = []
        for d in range(n_dims):
            dim_ranges.append(list(range(c[d]-1, c[d]+2)))
        for c_ in itertools.product(*dim_ranges): # product returns a tuple
            if c_ == c:
                continue
            if c_ in grid:
                n_actives += 1
        return n_actives
    
    def next_state(c):
        nonlocal grid, n_dims
        is_active = (c in grid)
        n_actives = n_active_neighboors(c)
        if is_active:
            return n_actives == 2 or n_actives == 3
        else:
            return n_actives == 3
    
    for cycle in range(cycles):      
        ngrid = set()
        nmin_coords = [0] * n_dims
        nmax_coords = [0] * n_dims
        dim_ranges = []
        for d in range(n_dims):
            dim_ranges.append(list(range(min_coords[d]-1, max_coords[d]+2)))
        for c_ in itertools.product(*dim_ranges):
            ns = next_state(c_)
            if ns:
                ngrid.add(c_)
                for d in range(n_dims):
                    nmin_coords[d] = min(c_[d], nmin_coords[d])
                    nmax_coords[d] = max(c_[d], nmax_coords[d])
        grid = ngrid
        min_coords = nmin_coords
        max_coords = nmax_coords
    
    return len(grid)

def test_p1():
    assert work_p2(sample_input.splitlines(), 3) == 112
test_p1()

def p1():
    print(work_p2(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input.splitlines(), 4) == 848
test_p2()

def p2():
    print(work_p2(fileinput.input(), 4))
p2()
