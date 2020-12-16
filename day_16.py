#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_16"]

sample_input_p1="""class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

sample_input_p2="""class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

def read_input(lines):
    fields = {}
    my_tickets = []
    nearby_tickets = []
    
    section=0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            section += 1
            continue
        
        if section == 0:
            name, ranges = line.split(": ")
            ranges = ranges.split(" or ")
            ranges = [r.split("-") for r in ranges]
            ranges = [(int(r[0]), int(r[1])) for r in ranges]
            fields[name] = ranges
        elif section == 1:
            if "ticket" in line:
                continue
            my_tickets = [int(i) for i in line.split(",")]
        elif section == 2:
            if "ticket" in line:
                continue
            nearby_tickets.append([int(i) for i in line.split(",")])

    return (fields, my_tickets, nearby_tickets)

def work_p1(lines):
    fields, my_tickets, nearby_tickets = read_input(lines)
    
    all_valids = set()
    for name, ranges in fields.items():
        for r in ranges:
            for i in range(r[0], r[1] + 1):
                all_valids.add(i)
    
    ret = 0
    for ticket in nearby_tickets:
        for i in ticket:
            if not i in all_valids:
                ret += i
    return ret

def solve_p2(fields, my_tickets, nearby_tickets):
    n_fields = len(my_tickets)
    field_names = fields.keys()
    
    possibilities = []
    for i in range(n_fields):
        possibilities.append(set(field_names))
    
    results = {}
    
    for ticket in nearby_tickets:
        for i in range(n_fields):
            v = ticket[i]
            for f, ranges in fields.items():
                if not f in possibilities[i]:
                    continue
                valid = False
                for r in ranges:
                    if v >= r[0] and v <= r[1]:
                        valid = True
                        break
                if not valid:
                    possibilities[i].remove(f)
    
    while True:
        found = set()
        for i in range(n_fields):
            if len(possibilities[i]) == 1:
                results[i] = possibilities[i].pop()
                for j in range(n_fields):
                    try:
                        possibilities[j].remove(results[i])
                    except:
                        pass
        if len(results) == n_fields:
            break
    
    return results
    
def work_p2(lines):
    fields, my_tickets, nearby_tickets = read_input(lines)
    
    all_valids = set()
    for name, ranges in fields.items():
        for r in ranges:
            for i in range(r[0], r[1] + 1):
                all_valids.add(i)
    
    tickets = []
    for ticket in nearby_tickets:
        valid = True
        for i in ticket:
            if not i in all_valids:
                valid = False
                break
        if valid:
            tickets.append(ticket)
    
    results = solve_p2(fields, my_tickets, tickets)
    
    ret = 1
    for i in range(len(results)):
        cls = results[i]
        if cls.startswith("departure"):
            ret *= my_tickets[i]
    return ret

def test_p1():
    assert work_p1(sample_input_p1.splitlines()) == 71
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
