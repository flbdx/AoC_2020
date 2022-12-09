#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

# basic tokenization
def tokenize(line):
    tokens = []
    in_number = None
    
    for c in line:
        if c == ' ':
            if in_number != None:
                tokens.append(int(in_number))
                in_number = None
        elif c in '+*()':
            if in_number != None:
                tokens.append(int(in_number))
                in_number = None
            tokens.append(c)
        else:
            in_number = c if in_number == None else (in_number + c)
    if in_number != None:
        tokens.append(int(in_number))
    return tokens

# replace parenthesized expressions by a sublist
def apply_parenthesis(tokens, s=0):
    r = []
    i = s
    while i < len(tokens):
        t = tokens[i]
        if t == '(':
            l, i = apply_parenthesis(tokens, i + 1)
            r.append(l)
        elif t == ')':
            return (r, i)
        else:
            r.append(t)
        i += 1
    return r

# apply from left to right
def rec_calc_p1(tokens):
    r = 0
    last_op = None
    
    for t in tokens:
        if t == '*':
            last_op = lambda x,y: x*y
        elif t == '+':
            last_op = lambda x,y: x+y
        else:
            if type(t) == list:
                v = rec_calc_p1(t)
            else:
                v = t
            if last_op != None:
                r = last_op(r, v)
                last_op = None
            else:
                r = v
    return r

# apply operators with exclusive precedence orders
def rec_calc_p2(tokens,operators):
    for op_char, op_func in operators:
        s = 0
        while s < (len(tokens) - 1):
            for s in range(s, len(tokens)):
                t = tokens[s]
                if t == op_char:
                    op1 = tokens[s-1]
                    op2 = tokens[s+1]
                    if type(op1) == list:
                        op1 = rec_calc_p2(op1, operators)
                    if type(op2) == list:
                        op2 = rec_calc_p2(op2, operators)
                    tokens = tokens[:s-1] + [op_func(op1, op2)] + tokens[s+2:]
                    break
    
    return tokens[0]

def work_p1(lines):
    r = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
    
        tokens = apply_parenthesis(tokenize(line))
        r += rec_calc_p1(tokens)
    return r

def work_p2(lines):
    r = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
    
        tokens = apply_parenthesis(tokenize(line))
        r += rec_calc_p2(tokens, [('+', lambda x, y: x+y), ('*', lambda x, y: x*y)])
    return r

def test_p1():
    assert work_p1(["2 * 3 + (4 * 5)"]) == 26
    assert work_p1(["5 + (8 * 3 + 9 + 3 * 4 * 3)"]) == 437
    assert work_p1(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]) == 12240
    assert work_p1(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]) == 13632
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(["2 * 3 + (4 * 5)"]) == 46
    assert work_p2(["5 + (8 * 3 + 9 + 3 * 4 * 3)"]) == 1445
    assert work_p2(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]) == 669060
    assert work_p2(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]) == 23340
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
