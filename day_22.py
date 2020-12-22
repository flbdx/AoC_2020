#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_22"]

sample_input="""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

def work_p1(lines):
    p1 = "Player 1"
    p2 = "Player 2"
    decks = {}
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("Player"):
            current_p = line[:-1]
        else:
            decks[current_p] = decks.get(current_p, []) + [int(line)]
    
    d1 = decks[p1]
    d2 = decks[p2]
    while len(d1) > 0 and len(d2) > 0:
        c1 = d1.pop(0)
        c2 = d2.pop(0)
        if c1 > c2:
            d1 += [c1, c2]
        else:
            d2 += [c2, c1]
    
    winner = p1 if len(d2) == 0 else p2
    ret = 0
    n_cards = len(decks[winner])
    for n in range(n_cards):
        ret += (n_cards - n) * decks[winner][n]
    return ret

def deck_signature(deck):
    return b''.join(v.to_bytes(1, 'little') for v in deck)

def rec_game(d1, d2, game):
    ss1 = deck_signature(d1)
    ss2 = deck_signature(d2)
    # a cache, not really necessary, I didn't know...
    cache_res = rec_game.cache.get(ss1+ss2, None)
    if cache_res != None:
        return cache_res
    
    p1_history = set()
    p2_history = set()
    
    rnd = 0
    while len(d1) > 0 and len(d2) > 0:
        rnd += 1
        s1 = deck_signature(d1)
        s2 = deck_signature(d2)
        if s1 in p1_history or s2 in p2_history:
            rec_game.cache[ss1 + ss2] = 1
            return 1
        p1_history.add(s1)
        p2_history.add(s2)
        
        c1 = d1.pop(0)
        c2 = d2.pop(0)
        if len(d1) >= c1 and len(d2) >= c2:
            round_winner = rec_game(d1[:c1], d2[:c2], game + 1)
        else:
            round_winner = 1 if c1 > c2 else 2
        
        if round_winner == 1:
            d1 += [c1, c2]
        else:
            d2 += [c2, c1]
    
    rec_game.cache[ss1 + ss2] = round_winner
    return round_winner

rec_game.cache = {}

def work_p2(lines):
    p1 = "Player 1"
    p2 = "Player 2"
    decks = {}
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("Player"):
            current_p = line[:-1]
        else:
            decks[current_p] = decks.get(current_p, []) + [int(line)]
            assert int(line) < 256
    
    d1 = decks[p1]
    d2 = decks[p2]
    n_cards = len(d1) + len(d2)
    
    winner = rec_game(d1, d2, 1)
    
    ret = 0
    for n in range(n_cards):
        ret += (n_cards - n) * (d1 if winner == 1 else d2)[n]
    return ret

def test_p1():
    assert work_p1(sample_input.splitlines()) == 306
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(sample_input.splitlines()) == 291
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
