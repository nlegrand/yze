from random import randrange

class Dice:
    def __init__(self, size=6):
        dice_sizes = [6, 8, 10, 12]
        d = [x for x in dice_sizes if x == size]
        if len(d) != 1:
            raise ValueError(f"Dice size should be one of 6, 8, 10, 12. {size} was provided.")
        self.size = size
    def throw(self):
        return randrange(1, self.size +1)
        
class DicePoolMutant:
    def __init__(self, attr=1, skill=0, gear=0):
        self.attr = attr
        self.skill = skill
        self.gear = gear
        self.thrown = False
        self.pushed = False
        self.result = {'attr': [], 'skill': [], 'gear': []}
        self.pushed_res = {'attr': [], 'skill': [], 'gear': []}
        
    def throw(self):
        if self.thrown:
            return self.result
        dice = Dice()
        for n in range(self.attr):
            self.result['attr'].append(dice.throw())
        for n in range(self.skill):
            self.result['skill'].append(dice.throw())
        for n in range(self.gear):
            self.result['gear'].append(dice.throw())
        self.thrown = True
        return self.result
    def push(self):
        if self.pushed:
            return self.pushed_res
        dice = Dice()
        for r in self.result['attr']:
            if r == 1 or r == 6:
                self.pushed_res['attr'].append(r)
            else:
                self.pushed_res['attr'].append(dice.throw())
        for r in self.result['skill']:
            if r == 6:
                self.pushed_res['skill'].append(r)
            else:
                self.pushed_res['skill'].append(dice.throw())
        for r in self.result['gear']:
            if r == 1 or r == 6:
                self.pushed_res['gear'].append(r)
            else:
                self.pushed_res['gear'].append(dice.throw())
        self.pushed = True
        return self.pushed_res
