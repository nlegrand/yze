from random import randrange


class Dice:
    def __init__(self, size=6):
        dice_sizes = [6, 8, 10, 12]
        d = [x for x in dice_sizes if x == size]
        if len(d) != 1:
            raise ValueError(f"Dice size should be one of 6, 8, 10, 12. {size} was provided.")
        self.size = size

    def throw(self):
        return randrange(1, self.size + 1)


class ArtefactDice(Dice):
    def throw(self):
        res = randrange(1, self.size + 1)
        successes = 0
        if 6 <= res <= 7:
            successes = 1
        elif 8 <= res <= 9:
            successes = 2
        elif 10 <= res <= 11:
            successes = 3
        elif res == 12:
            successes = 4
        return (res, successes)


class MutantDicePool:
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


class FBLDicePool:
    def __init__(self, attr=1, skill=0, gear=0, artefact=None):
        self.attr = attr
        self.skill = skill
        self.gear = gear
        self.artefact = artefact
        self.thrown = False
        self.pushed = False
        self.result = {'attr': [], 'skill': [], 'gear': [], 'artefact': 0}
        self.pushed_res = {'attr': [], 'skill': [], 'gear': [], 'artefact': 0}

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
        if self.artefact is not None:
            artefact_dice = ArtefactDice(size=self.artefact)
            self.result['artefact'] = artefact_dice.throw()
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
        if self.artefact is not None:
            if self.result['artefact'][1] == 0:
                artefact_dice = ArtefactDice(self.artefact)
                self.pushed_res['artefact'] = artefact_dice.throw()
            else:
                self.pushed_res['artefact'] = self.result['artefact']

        self.pushed = True
        return self.pushed_res


class AlienDicePool:

    def __init__(self, pool=1, stress=0):
        self.pool = pool
        self.stress = stress
        self.thrown = False
        self.pushed = False
        self.result = {'pool': [], 'stress': []}
        self.pushed_res = {'pool': [], 'stress': []}

    def throw(self):
        if self.thrown:
            return self.result
        dice = Dice()
        for n in range(self.pool):
            self.result['pool'].append(dice.throw())
        for n in range(self.stress):
            self.result['stress'].append(dice.throw())
        self.thrown = True
        return self.result

    def push(self):
        if self.pushed:
            return self.pushed_res
        dice = Dice()
        for r in self.result['pool']:
            if r == 6:
                self.pushed_res['pool'].append(r)
            else:
                self.pushed_res['pool'].append(dice.throw())
        for r in self.result['stress'] + [2]:
            if r == 6:
                self.pushed_res['stress'].append(r)
            else:
                self.pushed_res['stress'].append(dice.throw())

        self.pushed = True
        return self.pushed_res
