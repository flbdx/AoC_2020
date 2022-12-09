#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

sample_input="""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

sample_input_2="""shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

my_bag = "shiny gold"

class Bag(object):
    def __init__(self, name):
        self.name = name
        self.content = {}
        self.contained_by = []
    
    def __str__(self):
        return "[{0}] > {1}  < {2}".format(self.name, repr(self.content), repr(self.contained_by))

def parse_input(lines):
    bags = {}
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        container, content = line.split(" bags contain ")
        b = bags.get(container, Bag(container))
        if content != "no other bags.":
            content = content.split(", ")
            for c in content:
                dl = c.index(" ")
                dr = c.rindex(" ")
                n = int(c[0:dl])
                v = c[dl+1:dr]
                b.content[v] = n
                o = bags.get(v, Bag(v))
                o.contained_by.append(container)
                bags[v] = o
        bags[container] = b
    
    return bags


def work_p1(lines):
    bags = parse_input(lines)
    
    ret = set()
    to_check = list(bags[my_bag].contained_by)
    while len(to_check) != 0:
        b = to_check.pop()
        if not b in ret:
            ret.add(b)
            to_check += bags[b].contained_by
    
    return len(ret)
        
def work_p2(lines):
    bags = parse_input(lines)
    
    total = 0
    
    to_count = dict(bags[my_bag].content)
    while len(to_count) != 0:
        k, c = to_count.popitem()
        total += c
        for k, v in bags[k].content.items():
            to_count[k] = to_count.get(k, 0) + c * v
    return total

def test_p1():
    assert work_p1(sample_input.splitlines()) == 4
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input.splitlines()) == 32
    assert work_p2(sample_input_2.splitlines()) == 126
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
