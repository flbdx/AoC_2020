#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools
import functools
import operator

if len(sys.argv) == 1:
    sys.argv += ["input_09"]

sample_input="""35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

def parse_input(lines):
    numbers = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers.append(int(line))
    
    return numbers

def work_p1_(numbers, preamble_len):
    for i in range(preamble_len, len(numbers)):
        n = numbers[i]
        found = False
        for p in itertools.combinations(numbers[i-preamble_len:i], 2):
            if p[0] != p[1] and p[0] + p[1] == n:
                found = True
                #print(repr(n) + " == " + repr(p[0]) + " + " + repr(p[1]))
                break
        if not found:
            return (i, n)
    return (-1,-1)

def work_p1(lines, preamble_len=25):
    return work_p1_(parse_input(lines), preamble_len)[1]

def work_p2(lines, preamble_len=25):
    numbers = parse_input(lines)
    index, target = work_p1_(numbers, preamble_len)
    
    for w in range(2, index):
        for i in range(0, index - w):
            s = functools.reduce(operator.add, numbers[i:i+w])
            if s == target:
                return min(numbers[i:i+w]) + max(numbers[i:i+w])
    return -1
        

def test_p1():
    assert(work_p1(sample_input.splitlines(), 5) == 127)
test_p1()

def p1():
    print(work_p1(fileinput.input(), 25))
p1()

def test_p2():
    assert(work_p2(sample_input.splitlines(), 5) == 62)
test_p2()

def p2():
    print(work_p2(fileinput.input(), 25))
p2()
