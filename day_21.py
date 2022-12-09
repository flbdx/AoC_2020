#!/usr/bin/python3
#encoding: UTF-8

# Trust Me, It Works(TM)

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

sample_input="""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

class Food(object):
    def __init__(self, uid, line):
        self.uid = uid
        sep = " (contains "
        idx_sep = line.find(sep)
        if idx_sep == -1:
            self.ingredients = set(line.split(" "))
            self.known_allergens = set()
        else:
            self.ingredients = set(line[:idx_sep].split(" "))
            self.known_allergens = set(line[idx_sep + len(sep):-1].split(", "))
    
    def __repr__(self):
        return repr(self.uid) + " : " + repr(self.ingredients) + " " + repr(self.known_allergens)

class Plan(object):
    def __init__(self):
        self.foods = set()
        self.all_allergens = set()
        self.all_ingredients = set()
        self.foods_by_allergen = {}
        self.foods_by_ingredient = {}
        self.safe_ingredients = set()
        self.poisons = {}
    
    def input_foods(self, lines):
        lnumber = 0
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            lnumber += 1
            self.foods.add(Food(lnumber, line))
    
    def process_p1(self):
        # build some dictionaries with the foods and possible allergens associated with each ingredients 
        for f in self.foods:
            for i in f.ingredients:
                self.foods_by_ingredient[i] = self.foods_by_ingredient.get(i, []) + [f]
                self.all_ingredients.add(i)
            for a in f.known_allergens:
                self.foods_by_allergen[a] = self.foods_by_allergen.get(a, []) + [f]
                self.all_allergens.add(a)
        
        # search inconsistencies
        # if an ingredient has an allergen, it should be part of all foods which contains said allergen
        # we search non poisonous ingredients...
        for ingredient in self.all_ingredients:
            allergens_to_test = set()
            for food in self.foods_by_ingredient[ingredient]:
                allergens_to_test.update(food.known_allergens)
            maybe_poisons = False
            for allergen in allergens_to_test:
                maybe_poisons |= all(True if ingredient in food.ingredients else False for food in self.foods_by_allergen[allergen])
            if not maybe_poisons:
                self.safe_ingredients.add(ingredient)
    
    def p1(self):
        ret = 0
        for ingredient in self.safe_ingredients:
            ret += sum(1 for f in self.foods if ingredient in f.ingredients)
        return ret
    
    def process_p2(self):
        # remove the safe ingredients ...
        for food in self.foods:
            food.ingredients.difference_update(self.safe_ingredients)
        self.all_ingredients.difference_update(self.safe_ingredients)
        for ingredient in self.safe_ingredients:
            del self.foods_by_ingredient[ingredient]
        
        assert len(self.all_ingredients) == len(self.all_allergens)
        
        # our TODO list
        todo_allergens = set()
        todo_allergens.update(self.all_allergens)
        
        def assign_allergen(ingredient, allergen):
            self.poisons[allergen] = ingredient
            todo_allergens.difference_update(set([allergen]))
            for food in self.foods:
                food.ingredients.difference_update(set([ingredient]))
                food.known_allergens.difference_update(set([allergen]))
        
        while len(todo_allergens) != 0:
            for food in self.foods:
                if len(food.ingredients) == 1 and len(food.known_allergens) == 1:
                    assign_allergen(food.ingredients.pop(), food.known_allergens.pop())
            
            if len(todo_allergens) == 0:
                break
            
            for allergen in todo_allergens:
                candidates = {}
                n_foods = 0
                for food in self.foods_by_allergen[allergen]:
                    if len(food.ingredients) > 0:
                        n_foods += 1
                        for i in food.ingredients:
                            candidates[i] = candidates.get(i, 0) + 1
                candidates = [c for c, n in candidates.items() if n == n_foods]
                if len(candidates) == 1:
                    assign_allergen(candidates[0], allergen)
                    # break because we just borked our iterator over todo_allergens
                    break

        #print(self.poisons)
    
    def p2(self):
        return ",".join([self.poisons[k] for k in sorted(self.poisons.keys())])

def test():
    plan = Plan()
    plan.input_foods(sample_input.splitlines())
    plan.process_p1()
    assert plan.p1() == 5
    plan.process_p2()
    assert plan.p2() == "mxmxvkd,sqjhc,fvjkl"
test()

def p():
    plan = Plan()
    plan.input_foods(fileinput.input())
    plan.process_p1()
    print(plan.p1())
    plan.process_p2()
    print(plan.p2())
p()
