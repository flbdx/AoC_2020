#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

sample_input_p1="""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

class VM(object):
    def __init__(self, asm_lines):
        self.instructions = []
        self.reset()
        
        for line in asm_lines:
            line = line.strip()
            if len(line) == 0:
                continue
            instr, op1 = line.split(" ")
            op1 = int(op1)
            
            self.instructions.append((getattr(VM, "do_" + instr), op1))
            
    def run_one(self):
        instr, op1 = self.instructions[self.ip]
        instr(self, op1)
        return (self.ip, self.ip < 0 or self.ip >= len(self.instructions))
    
    def reset(self):
        self.ip = 0
        self.acc = 0
    
    def do_acc(self, param):
        self.acc += param
        self.ip += 1
    
    def do_jmp(self, param):
        self.ip += param
    
    def do_nop(self, param):
        self.ip += 1

def work_p1(lines):
    vm = VM(lines)
    ips = set()

    while True:
        ip, done = vm.run_one()
        if (ip in ips) or done:
            break
        ips.add(ip)
    return vm.acc

def work_p2(lines):
    lines = list(lines)
    for i in range(0, len(lines)):
        l = lines[i].strip()
        if len(l) == 0:
            continue
        if l[0:3] == "nop":
            nlines = list(lines)
            nlines[i] = "jmp" + l[3:]
        elif l[0:3] == "jmp":
            nlines = list(lines)
            nlines[i] = "nop" + l[3:]
        else:
            continue
        
        vm = VM(nlines)
        ips = set()

        while True:
            ip, done = vm.run_one()
            if (ip in ips):
                break
            if done:
                return vm.acc
            ips.add(ip)
    
    return None

def test_p1():
    assert work_p1(sample_input_p1.splitlines()) == 5
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input_p1.splitlines()) == 8
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
