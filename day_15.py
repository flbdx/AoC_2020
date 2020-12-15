#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_15"]

sample_sequence="""0,3,6"""

# good enough?
def work_p1(lines, target=2020):
    start_sequence = [int(v) for v in list(lines)[0].strip().split(",")]
    positions = {}
    last_one = None
    
    n = 0
    for last_one in start_sequence:
        n += 1
        p = positions.setdefault(last_one, [-1,-1])
        p[0] = p[1]
        p[1] = n
    
    # p is a mutable list
    # this will work like a reference to the stored value
    while n != target:
        n += 1
        last_one = 0 if p[0] == -1 else p[1] - p[0]
        p = positions.setdefault(last_one, [-1,-1])
        p[0] = p[1]
        p[1] = n
    
    return last_one

def test_p1():
    assert work_p1(sample_sequence.splitlines()) == 436
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

#def test_p2():
    #assert work_p1(sample_sequence.splitlines(), 30000000) == 175594
#test_p2()

def p2():
    print(work_p1(fileinput.input(), 30000000))
p2()
