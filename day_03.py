#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

test_input = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

def work_p1(lines, step_r = 3, step_d = 1):
    world = {}
    width = 0
    height = 0
    for y, line in enumerate(lines):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            world[x,y] = True if c == '#' else False
            width = max(width, x + 1)
        height = max(height, y + 1)
    
    ret = 0
    x = step_r
    y = step_d
    while y < height:
        if world[x % width, y]:
            ret += 1
        x += step_r
        y += step_d
    return ret

def work_p2(lines):
    r = 1
    lines = list(lines)
    r *= work_p1(lines, 1, 1)
    r *= work_p1(lines, 3, 1)
    r *= work_p1(lines, 5, 1)
    r *= work_p1(lines, 7, 1)
    r *= work_p1(lines, 1, 2)
    return r

def test_p1():
    assert work_p1(test_input.splitlines()) == 7
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()
    
def test_p2():
    assert work_p2(test_input.splitlines()) == 336
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
    
