#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

if len(sys.argv) == 1:
    sys.argv += ["input_14"]
    
sample_input_1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

sample_input_2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

def read_mask_p1(mask):
    assert len(mask) == 36
    mask_or, mask_and = 0, (1 << 37) - 1
    for i in range(0, 36):
        c = mask[35-i]
        if c == '1':
            mask_or += (1 << i)
        elif c == '0':
            mask_and -= (1 << i)
    return (mask_or, mask_and)


def work_p1(lines):
    mask_or, mask_and = 0, 0
    mem = {}
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        m, v = line.split(" = ")
        if m == "mask":
            mask_or, mask_and = read_mask_p1(v)
        else:
            m = int(m[4:-1])
            v = (int(v) | mask_or) & mask_and
            mem[m] = v
    return sum(mem.values())

def read_mask_p2(mask):
    assert len(mask) == 36
    mask_or, mask_and, mask_float = 0, (1 << 37) - 1, []
    for i in range(0, 36):
        c = mask[35-i]
        if c == '1':
            mask_or += (1 << i)
        elif c == 'X':
            mask_and -= (1 << i)
            mask_float.append(1 << i)
    return (mask_or, mask_and, mask_float)

def work_p2(lines):
    mem = {}
    mask_or, mask_and, mask_float = 0, (1 << 37) - 1, []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        m, v = line.split(" = ")
        if m == "mask":
            mask_or, mask_and, mask_float = read_mask_p2(v)
        else:
            m = (int(m[4:-1])| mask_or) & mask_and
            v = int(v)
            mem[m] = v
            for i in range(1, len(mask_float) + 1):
                for s in itertools.combinations(mask_float, i):
                    mem[m + sum(s)] = v
    return sum(mem.values())

def test_p1():
    assert work_p1(sample_input_1.splitlines()) == 165
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input_2.splitlines()) == 208
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
