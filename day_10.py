#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

sample_input_1="""16
10
15
5
1
11
7
19
6
12
4"""
sample_input_2="""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

def parse_input(lines):
    numbers = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers.append(int(line))
    return numbers

def work_p1(lines):
    numbers = parse_input(lines)
    numbers = sorted(numbers)
    
    first_joltage = 0
    rated_joltage = max(numbers) + 3
    numbers = [first_joltage] + numbers + [rated_joltage]
    
    stats = {}
    for n in range(1, len(numbers)):
        d = numbers[n] - numbers[n - 1]
        stats[d] = stats.get(d, 0) + 1
    return stats[1] * stats[3]

def work_p2(lines):
    numbers = parse_input(lines)
    numbers = sorted(numbers)
    
    first_joltage = 0
    rated_joltage = max(numbers) + 3
    numbers = [first_joltage] + numbers + [rated_joltage]
    
    # there is no chain with a diff of 2
    # adapters can only be removed when there is at least 2 links of 1 joltage diff
    # for my input the largest chain of 1 joltage diff is 5 numbers (4 links)
    res = 1
    chain_1_len = 0
    for n in range(1, len(numbers)):
        d = numbers[n] - numbers[n - 1]
        if d == 1:
            chain_1_len += 1
        else:
            if chain_1_len == 2:
                res *= 2
            elif chain_1_len == 3:
                res *= 4
            elif chain_1_len == 4:
                res *= 7
            elif chain_1_len > 4:
                assert(False)
            chain_1_len = 0
    return res

def test_p1():
    assert work_p1(sample_input_1.splitlines()) == 35
    assert work_p1(sample_input_2.splitlines()) == 220
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input_1.splitlines()) == 8
    assert work_p2(sample_input_2.splitlines()) == 19208
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
