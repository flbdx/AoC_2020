#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

sample_input="""389125467"""

def work_p1(lines, moves):
    nxt = None
    l = 0
    for line in lines:
        line = line.strip()
        l = len(line)
        nxt = [None] * (l + 1)
        for i in range(l):
            nxt[int(line[i])] = int(line[(i+1)%l])
        cup = int(line[0])
        break
    
    for mov in range(moves):
        picks = [nxt[cup], None, None]
        picks[1] = nxt[picks[0]]
        picks[2] = nxt[picks[1]]
        
        dst_cup = l if cup == 1 else (cup - 1)
        while dst_cup in picks:
            dst_cup = l if dst_cup == 1 else (dst_cup - 1)
        o = nxt[dst_cup]
        nxt[cup] = nxt[picks[2]]
        nxt[dst_cup] = picks[0]
        nxt[picks[2]] = o
        cup = nxt[cup]
    
    ret = ""
    cup = 1
    for i in range(1, l):
        ret += repr(nxt[cup])
        cup = nxt[cup]
    return ret

def work_p2(lines, moves):
    limit = 1000000
    nxt = None
    l = 0
    for line in lines:
        line = line.strip()
        l = len(line)
        nxt = [None] * (limit + 1)
        for i in range(l):
            nxt[int(line[i])] = int(line[(i+1)%l])
        nxt[int(line[l-1])] = l+1
        for i in range(l + 1, limit):
            nxt[i] = i + 1
        nxt[limit] = int(line[0])
        cup = int(line[0])
        break
    l = limit
    
    # no change from part 1
    for mov in range(moves):
        pick0 = nxt[cup]
        pick1 = nxt[pick0]
        pick2 = nxt[pick1]
        
        dst_cup = l if cup == 1 else (cup - 1)
        while dst_cup == pick0 or dst_cup == pick1 or dst_cup == pick2:
            dst_cup = l if dst_cup == 1 else (dst_cup - 1)
        nxt[cup], nxt[pick2], nxt[dst_cup] = nxt[pick2], nxt[dst_cup], pick0
        cup = nxt[cup]
    
    return nxt[1] * nxt[nxt[1]]

def test_p1():
    assert work_p1([sample_input], 10) == "92658374"
    assert work_p1([sample_input], 100) == "67384529"
test_p1()

def p1():
    print(work_p1(list(fileinput.input()), 100))
p1()

def test_p2():
    assert work_p2([sample_input], 10000000) == 149245887792
test_p2()

def p2():
    print(work_p2(list(fileinput.input()), 10000000))
p2()
