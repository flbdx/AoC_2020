#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import functools
import operator

if len(sys.argv) == 1:
    sys.argv += ["input_13"]
    
# all my input numbers are prime

sample_input="""939
7,13,x,x,59,x,31,19"""

def work_p1(input_):
    lines = [l.strip() for l in input_]
    target = int(lines[0])
    ids = lines[1].split(",")
    ids = [int(c) for c in ids if c != 'x']
    
    best = None
    for id in ids:
        q, r = divmod(target, id)
        r = target if r == 0 else (id - r)
        if best == None or r < best[1]:
            best = (id, r)
    return best[0] * best[1]
    

def work_p2(input_):
    lines = [l.strip() for l in input_]
    ids = lines[1].split(",")
    
    mods = []
    rems = []
    for i in range(0, len(ids)):
        if ids[i] == 'x':
            continue
        id = int(ids[i])
        mods.append(id)
        rems.append((id - i) % id)
    
    # https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_des_restes_chinois#Algorithme
    n = functools.reduce(operator.mul, mods)
    s = 0
    for i in range(0, len(mods)):
        n_i = n // mods[i]
        v_i = (n_i ** (mods[i] - 2)) % mods[i] # v_i * n_i = 1 mod n_i
        e_i = n_i * v_i
        s += rems[i] * e_i
    return s % n

def test_p1():
    assert work_p1(sample_input.splitlines()) == 295
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input.splitlines()) == 1068781
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
