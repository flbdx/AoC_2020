#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools
import functools
import operator

if len(sys.argv) == 1:
    sys.argv += ["input_01"]

def work(lines, length):
    numbers = [int(l) for l in lines if len(l) > 0]
    for t in itertools.combinations(numbers, length):
        if functools.reduce(operator.add, t) == 2020:
            return functools.reduce(operator.mul, t)
    return -1

test_input="""1721
979
366
299
675
1456"""

def test_p1():
    assert(work(test_input.splitlines(), 2) == 514579)

test_p1()

def p1():
    print(work(fileinput.input(), 2))
p1()

def test_p2():
    assert(work(test_input.splitlines(), 3) == 241861950)

test_p2()

def p2():
    print(work(fileinput.input(), 3))
p2()
