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
    seen_numbers = set()
    positions = {}
    last_one = None
    last_one_was_seen = False
    
    n = 0
    for i in start_sequence:
        n += 1
        positions[i] = (positions.get(i, (0,0))[1], n)
        last_one = i
        last_one_was_seen = last_one in seen_numbers
        if not last_one_was_seen:
            seen_numbers.add(last_one) # testing and updating in one pass would be great
    
    while n != target:
        n += 1
        if last_one_was_seen:
            a, b = positions[last_one]
            last_one = b - a
            last_one_was_seen = last_one in seen_numbers
        else:
            seen_numbers.add(last_one)
            last_one = 0
            last_one_was_seen = True
        positions[last_one] = (positions.get(last_one, (0,0))[1], n)
    
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
