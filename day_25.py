#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_25"]

#$ openssl prime 20201227
#1343F0B (20201227) is prime
prime = 20201227

def find_priv(sn, pub):
    l = 1
    v = sn
    while v != pub:
        v = (v * sn) % prime
        l += 1
    return l

def solve_p1(pub1, pub2):
    priv1 = find_priv(7, pub1)
    secret = pow(pub2, priv1, prime)
    return secret

def test_p1():
    assert solve_p1(5764801, 17807724) == 14897079
test_p1()

def p1():
    lines = list(fileinput.input())
    print(solve_p1(int(lines[0]), int(lines[1])))
p1()
