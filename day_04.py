#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

test_input = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

def test_passport_p1(fields):
    mandatory_fields = {"byr": False, "iyr": False, "eyr": False, "hgt": False, "hcl": False, "ecl": False, "pid": False}
    optional_field = {"cid": False}
    
    for k, v in fields.items():
        if k in mandatory_fields.keys():
            mandatory_fields[k] = True
        elif k in optional_field.keys():
            optional_field[k] = True
    
    return all(mandatory_fields.values())

def test_passport_p2(fields):
    mandatory_fields = {"byr": False, "iyr": False, "eyr": False, "hgt": False, "hcl": False, "ecl": False, "pid": False}
    optional_field = {"cid": False}
    
    for k, v in fields.items():
        if k in mandatory_fields.keys():
            mandatory_fields[k] = v
        elif k in optional_field.keys():
            optional_field[k] = v
    
    if not all(mandatory_fields.values()):
        return False
    
    
    try:
        #byr (Birth Year) - four digits; at least 1920 and at most 2002.
        v = mandatory_fields["byr"]
        if len(v) != 4 or int(v) < 1920 or int(v) > 2002:
            return False
        #iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        v = mandatory_fields["iyr"]
        if len(v) != 4 or int(v) < 2010 or int(v) > 2020:
            return False
        #eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        v = mandatory_fields["eyr"]
        if len(v) != 4 or int(v) < 2020 or int(v) > 2030:
            return False
        #hgt (Height) - a number followed by either cm or in:
        #   If cm, the number must be at least 150 and at most 193.
        #   If in, the number must be at least 59 and at most 76.
        v = mandatory_fields["hgt"]
        u = v[-2:]
        n = int(v[:-2])
        if u == "cm":
            if n < 150 or n > 193:
                return False
        elif u == "in":
            if n < 59 or n > 76:
                return False
        else:
            return False
        #hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        v = mandatory_fields["hcl"]
        u = v[0]
        n = int(v[1:], base=16)
        if len(v) != 7 or u != "#" or n >= 256**3:
            return False
        #ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        v = mandatory_fields["ecl"]
        if not v in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return False
        #pid (Passport ID) - a nine-digit number, including leading zeroes.
        v = mandatory_fields["pid"]
        if len(v) != 9 or int(n) < 0:
            return False
        
    except:
        return False
    #cid (Country ID) - ignored, missing or not.
    
    return True

def work(lines, valid_func):
    n = 0
    fields = {}
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            if len(fields) == 0:
                break
            else:
                if valid_func(fields):
                    n += 1
                fields = {}
        
        for entry in line.split(" "):
            if len(entry) == 0:
                continue
            k, v = entry.split(":")
            fields[k] = v
    return n

def test_p1():
    assert(work(test_input.splitlines(), test_passport_p1)) == 2
test_p1()

def p1():
    print(work(fileinput.input(), test_passport_p1))
p1()

def p2():
    print(work(fileinput.input(), test_passport_p2))
p2()
