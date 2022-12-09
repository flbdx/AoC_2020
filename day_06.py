#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_06"]

def work_p1(lines):
    ret = 0
    
    group_yes = set()
    
    def count_group():
        nonlocal group_yes, ret
        ret += len(group_yes)
        group_yes = set()
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            count_group()
        else:
            for c in line:
                group_yes.add(c)
    
    count_group()
    
    return ret

def work_p2(lines):
    ret = 0
    
    group_yes = {}
    group_size = 0
    
    def count_group():
        nonlocal group_yes, group_size, ret
        for k, v in group_yes.items():
            if v == group_size:
                ret += 1
        
        group_yes = {}
        group_size = 0
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            count_group()
        else:
            for c in line:
                group_yes[c] = group_yes.get(c, 0) + 1
            group_size += 1
    
    count_group()
    
    return ret

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
