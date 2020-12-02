#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_02"]

test_input="""1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

def work_p1(lines):
    valids = 0
    for line in lines:
        if len(line) == 0:
            continue
        policy, pwd = line.split(": ")
        policy, letter = policy.split(" ")
        pol_min, pol_max = map(int, policy.split("-"))
        
        n = 0
        for c in pwd:
            if c == letter:
                n += 1
        
        if n >= pol_min and n <= pol_max:
            valids += 1
    
    return valids

def work_p2(lines):
    valids = 0
    for line in lines:
        if len(line) == 0:
            continue
        policy, pwd = line.split(": ")
        policy, letter = policy.split(" ")
        pol_p1, pol_p2 = map(int, policy.split("-"))
        
        if (pwd[pol_p1 - 1] == letter) ^ (pwd[pol_p2 - 1] == letter):
            valids += 1
    
    return valids

def test_p1():
    assert work_p1(test_input.splitlines()) == 2
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(test_input.splitlines()) == 1
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
