#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

def read_pass_id(string):
    n = 0
    for c in string:
        n *= 2
        if c == 'B' or c == 'R':
            n += 1
    return n

def test_p1():
    assert(read_pass_id("BFFFBBFRRR") == 567)
    assert(read_pass_id("FFFBBBFRRR") == 119)
    assert(read_pass_id("BBFFBBFRLL") == 820)
test_p1()

def work_p1(lines):
    r = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        r = max(r, read_pass_id(line))
    return r

def work_p2(lines):
    all_ids = set()
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        all_ids.add(read_pass_id(line))
    first = min(all_ids)
    last = max(all_ids)
    for seat in range(first + 1, last):
        if not seat in all_ids and (seat + 1) in all_ids and (seat - 1) in all_ids:
            return seat
    

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
