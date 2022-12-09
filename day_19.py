#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_19"]
    
sample_input_p1="""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

sample_input_p2="""42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

class Rule(object):
    all_rules = {}
    
    def __init__(self):
        self.number = -1
        self.expression = None
        self.depends_on = set()
        self.dependency_off = set()
        
        self.regexp_str = None
    
    def set_rule(self, number, expr):
        l = []
        self.expression = []
        self.number = number
        for t in expr.split(" "):
            if t == '|':
                self.expression.append(l)
                l = []
            else:
                t = eval(t)
                l.append(t)
                if type(t) == int:
                    self.depends_on.add(t)
                    Rule.all_rules.setdefault(t, Rule()).dependency_off.add(self.number)
        if len(l) != 0:
            self.expression.append(l)
        
        if len(self.expression) == 1 and len(self.expression[0]) == 1 and type(self.expression[0][0]) == str: # literal
            self.regexp_str = self.expression[0][0]
    
    def is_ready(self):
        return self.regexp_str != None
    
    def get_pattern(self):
        return self.regexp_str
    
    def try_build_regexp(self):
        if not all(Rule.all_rules[n].is_ready() for n in self.depends_on):
            return False
        s = ""
        outer_parenthesis = (len(self.expression) > 1)
        if outer_parenthesis:
            s += "("
        first = True
        for g in self.expression:
            if not first:
                s += "|"
            else:
                first = False
            inner_parenthesis = ('|' in g)
            if inner_parenthesis:
                s += "("
            for t in g:
                if type(t) == int:
                    s += Rule.all_rules[t].regexp_str
                else:
                    s += t
            if inner_parenthesis:
                s += ")"
        if outer_parenthesis:
            s += ")"
        self.regexp_str = s
        return True
    
    def __repr__(self):
        return repr(self.number)+": "+repr(self.expression)+" > "+repr(self.depends_on)+" < "+repr(self.dependency_off)
        #return repr(self.number)+": "+repr(self.expression)+ " # " + repr(self.regexp_str)

def work(lines, part=1):
    Rule.all_rules.clear()
    input_part = 0
    
    inputs = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            input_part += 1
            continue
        
        if input_part == 0:
            rule_number, expr = line.split(": ")
            rule_number = int(rule_number)
            
            # the target is now at least one "42" pattern followed by n "42" patterns and n "31" patterns (n >= 1)
            # I will use up to 5 repetition for the "8" rule, and up to 4 for the "11" rule
            if part == 2 and rule_number == 8:
                Rule.all_rules.setdefault(rule_number, Rule()).set_rule(rule_number, "42 | 42 42 | 42 42 42 | 42 42 42 42 | 42 42 42 42 42")
            elif part == 2 and rule_number == 11:
                Rule.all_rules.setdefault(rule_number, Rule()).set_rule(rule_number, "42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31")
            else:
                Rule.all_rules.setdefault(rule_number, Rule()).set_rule(rule_number, expr)
        else:
            inputs.append(line)
    
    to_parse = list(Rule.all_rules.keys())
    while len(to_parse) != 0:
        rnumber = to_parse.pop(0)
        r = Rule.all_rules[rnumber]
        if r.is_ready():
            continue
        if not r.try_build_regexp():
            to_parse.append(rnumber)
    
    #print(Rule.all_rules[0].get_pattern())
    pattern = re.compile(Rule.all_rules[0].get_pattern())
    
    ret = 0
    for line in inputs:
        if pattern.fullmatch(line) != None:
            ret += 1
    return ret

def test_p1():
    assert work(sample_input_p1.splitlines()) == 2
test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def test_p2():
    assert work(sample_input_p2.splitlines(), part=2) == 12
test_p2()

def p2():
    print(work(fileinput.input(), part=2))
p2()
