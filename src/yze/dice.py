# Copyright (c) Nicolas Legrand <nicolas.legrand@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from random import randrange


class SimpleDie:
    """Basic class for YZE dice
    """
    def __init__(self, size=6):
        """Check size of the dice, 6 by default or 8, 10, 12. Return a dice
        object with a size attribute.
        """
        dice_sizes = [6, 8, 10, 12]
        d = [x for x in dice_sizes if x == size]
        if len(d) != 1:
            raise ValueError(f"Dice size should be one of 6, 8, 10, 12. {size} was provided.")
        self.size = size

    def throw(self):
        """Generate a pseudo-random number in the range of the SimpleDie
        Object. It returns an int.
        """
        return randrange(1, self.size + 1)


class ArtefactDie(SimpleDie):
    """Artefact dice are used in Forbidden Lands RPG.
    """
    def throw(self):
        """Artefact dice succeeds on 6+. You have more successes with higher
        result. Returns a tuple with the results and the successes
        obtained. The success rate is different from Step dice.
        """
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


class StepDie(SimpleDie):
    """Step dice is the dice system used un Twilight 2000 and Blade Runner
    RPG.
    """
    def throw(self):
        """Step dice suceeds on 6+. You have more successes with higher
        result. Returns a tuple with the results and the successes
        obtained. The success rate is different from ArtefactDie
        """
        res = randrange(1, self.size + 1)
        successes = 0
        if 6 <= res <= 9:
            successes = 1
        elif 10 <= res <= 12:
            successes = 2
        return (res, successes)


class HitLocationDie():
    """Twilight 2000 use a special die to determine the hit location.
    """
    def __init__(self):
        """d6  Hit Location
        1   Legs
        2-4 Torso
        5   Arm
        6   Head
        """
        self.hit_location = ["Leg", "Torso", "Torso", "Torso", "Arm", "Head"]
        self.die_size = 6

    def throw(self):
        """Roll for hit location
        """
        return self.hit_location[randrange(self.die_size)]


class MutantDicePool:
    """Emulate the dice pool found in Mutant: Year Zero. The
    MutantDicePool object can only make one throw and then one
    push. To make another throw, you’ll need to create a new object.
    """
    def __init__(self, attr=1, skill=0, gear=0):
        """Build the object. Make two dicts of lists to store results. thrown
        and push are state attributes.
        """
        self.attr = attr
        self.skill = skill
        self.gear = gear
        self.thrown = False
        self.pushed = False
        self.result = {'attr': [], 'skill': [], 'gear': []}
        self.pushed_res = {'attr': [], 'skill': [], 'gear': []}

    def throw(self):
        """Throw the dice and set the thrown state on.
        """
        if self.thrown:
            return self.result
        dice = SimpleDie()
        for n in range(self.attr):
            self.result['attr'].append(dice.throw())
        for n in range(self.skill):
            self.result['skill'].append(dice.throw())
        for n in range(self.gear):
            self.result['gear'].append(dice.throw())
        self.thrown = True
        return self.result

    def push(self):
        """Push the dice and set the thrown state on.
        """
        if self.pushed:
            return self.pushed_res
        dice = SimpleDie()
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
    """Emulate the dice pool found in Forbidden Lands. The FBLDicePool
    object can only make one throw and then one push. To make another
    throw, you’ll need to create a new object.
    """
    def __init__(self, attr=1, skill=0, gear=0, artefact=None):
        """As MutantDicePool, with artefact. Artefact dice is not a list, but
        an int, showing how many results you get.
        """
        self.attr = attr
        self.skill = skill
        self.gear = gear
        self.artefact = artefact
        self.thrown = False
        self.pushed = False
        self.multipushed = False
        self.result = {'attr': [], 'skill': [], 'gear': [], 'artefact': 0}
        self.pushed_res = {'attr': [], 'skill': [], 'gear': [], 'artefact': 0}
        self.multipushed_res = {'attr': [], 'skill': [], 'gear': [], 'artefact': 0}

    def throw(self):
        """Throw the dice and set the thrown state on.
        """
        if self.thrown:
            return self.result
        dice = SimpleDie()
        for n in range(self.attr):
            self.result['attr'].append(dice.throw())
        for n in range(self.skill):
            self.result['skill'].append(dice.throw())
        for n in range(self.gear):
            self.result['gear'].append(dice.throw())
        if self.artefact is not None:
            artefact_dice = ArtefactDie(size=self.artefact)
            self.result['artefact'] = artefact_dice.throw()
        self.thrown = True
        return self.result

    def push(self):
        """Push the dice and set the pushed state on.
        """
        if self.pushed:
            return self.pushed_res
        dice = SimpleDie()
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
                artefact_dice = ArtefactDie(self.artefact)
                self.pushed_res['artefact'] = artefact_dice.throw()
            else:
                self.pushed_res['artefact'] = self.result['artefact']

        self.pushed = True
        return self.pushed_res

    def multipush(self):
        """Dwarves can multipush without limit...
        """
        if not self.pushed and self.thrown:
            return self.push(self)
        if self.multipushed:
            """Permit multipush to be repeated to the point were you have 6 or 1
            everywhere. This is destructive, we don’t keep track of
            all results.
            """
            self.pushed_res = self.multipushed_res
            self.multipushed_res = {'attr': [], 'skill': [], 'gear': [], 'artefact': 0}
        dice = SimpleDie()
        for r in self.pushed_res['attr']:
            if r == 1 or r == 6:
                self.multipushed_res['attr'].append(r)
            else:
                self.multipushed_res['attr'].append(dice.throw())
        for r in self.pushed_res['skill']:
            if r == 6:
                self.multipushed_res['skill'].append(r)
            else:
                self.multipushed_res['skill'].append(dice.throw())
        for r in self.pushed_res['gear']:
            if r == 1 or r == 6:
                self.multipushed_res['gear'].append(r)
            else:
                self.multipushed_res['gear'].append(dice.throw())
        if self.artefact is not None:
            if self.pushed_res['artefact'][1] == 0:
                artefact_dice = ArtefactDie(self.artefact)
                self.multipushed_res['artefact'] = artefact_dice.throw()
            else:
                self.multipushed_res['artefact'] = self.pushed_res['artefact']
        self.multipushed = True
        return self.multipushed_res


class AlienDicePool:
    """Emulate the Alien dice pool throw, push and multipush."""
    def __init__(self, pool=1, stress=0):
        self.pool = pool
        self.stress = stress
        self.thrown = False
        self.pushed = False
        self.multipushed = False
        self.result = {'pool': [], 'stress': []}
        self.pushed_res = {'pool': [], 'stress': []}
        self.multipushed_res = {'pool': [], 'stress': []}

    def throw(self):
        """Throw the dice and set the thrown state on.
        """   
        if self.thrown:
            return self.result
        dice = SimpleDie()
        for n in range(self.pool):
            self.result['pool'].append(dice.throw())
        for n in range(self.stress):
            self.result['stress'].append(dice.throw())
        self.thrown = True
        return self.result

    def push(self):
        """Push the dice adding a stress die and set the pushed state on.
        """
        if self.pushed:
            return self.pushed_res
        dice = SimpleDie()
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

    def multipush(self):
        """Push the dice a second time adding a stress die and set the
        multipushed state on.
        """
        if self.multipushed:
            return self.multipushed_res
        dice = SimpleDie()
        for r in self.pushed_res['pool']:
            if r == 6:
                self.multipushed_res['pool'].append(r)
            else:
                self.multipushed_res['pool'].append(dice.throw())
        for r in self.pushed_res['stress'] + [2]:
            if r == 6:
                self.multipushed_res['stress'].append(r)
            else:
                self.multipushed_res['stress'].append(dice.throw())

        self.multipushed = True
        return self.multipushed_res


class Twilight2000DicePool:
    """Emulate the Twilight 2000 dice pool, ammo throw, push
    """
    def __init__(self, attr="D", skill=None, ammo=None):
        self.attr = attr
        self.skill = skill
        self.ammo = ammo
        self.thrown = False
        self.pushed = False
        self.multipushed = False
        self.hit_locationed = False
        self.hit_location_res = ''
        self.result = {}
        self.pushed_res = {}
        self.multipushed_res = {}

    def value_to_dice(self, value):
        """Return the StepDie object according to the attribute or
        skill value.
        """
        match value:
            case "A":
                return self.make_dice_and_throw(dice_size=12)
            case "B":
                return self.make_dice_and_throw(dice_size=10)
            case "C":
                return self.make_dice_and_throw(dice_size=8)
            case "D":
                return self.make_dice_and_throw(dice_size=6)
            case None:
                return None
            case _:
                raise ValueError

    def make_dice_and_throw(self, dice_size):
        d = StepDie(size=dice_size)
        return d.throw()

    def throw(self):
        """Throw the dice and set the thrown state on.
        """
        if self.thrown:
            return self.result
        attr_res = self.value_to_dice(value=self.attr)
        skill_res = self.value_to_dice(value=self.skill)
        if self.ammo:
            self.result['ammo'] = []
            d = SimpleDie()
            for a in range(self.ammo):
                self.result['ammo'].append(d.throw())
        if attr_res:
            self.result['attr'] = attr_res
        if skill_res:
            self.result['skill'] = skill_res
        self.thrown = True
        return self.result

    def hit_location(self):
        if self.hit_locationed:
            return self.hit_location_res
        self.hit_location_res = HitLocationDie().throw()
        self.hit_locationed = True
        return self.hit_location_res

    def check_res_and_push(self, res, value):
        """Push the dice unless it already has two success or one
        success while even_one_success is set to False
        """
        if res[1] >= 1:
            return res
        return self.value_to_dice(value=value)

    def push(self):
        """Push all dice you can push
        """
        if self.pushed:
            return self.pushed_res
        if 'attr' in self.result:
            self.pushed_res['attr'] = self.check_res_and_push(self.result['attr'], self.attr)
        if 'skill' in self.result:
            self.pushed_res['skill'] = self.check_res_and_push(self.result['skill'], self.skill)
        if 'ammo' in self.result:
            d = SimpleDie()
            self.pushed_res['ammo'] = []
            for r in self.result['ammo']:
                if r == 1 or r == 6:
                    self.pushed_res['ammo'].append(r)
                else:
                    self.pushed_res['ammo'].append(d.throw())
        self.pushed = True
        return self.pushed_res


class BladeRunnerDicePool():
    """Emulate the Blade Runner dice pool avantage, disavantage,
    throw, push and multipush."""
    def __init__(self, attr="D", skill="D", advantage=None):
        self.attr = attr
        self.skill = skill
        self.advantage = advantage
        self.thrown = False
        self.pushed = False
        self.multipushed = False
        self.result = {}
        self.pushed_res = {}
        self.multipushed_res = {}

    def value_to_dice(self, value):
        """Return the StepDie object according to the attribute or
        skill value.
        """
        match value:
            case "A":
                return self.make_dice_and_throw(dice_size=12)
            case "B":
                return self.make_dice_and_throw(dice_size=10)
            case "C":
                return self.make_dice_and_throw(dice_size=8)
            case "D":
                return self.make_dice_and_throw(dice_size=6)
            case None:
                return None
            case _:
                raise ValueError

    def make_dice_and_throw(self, dice_size):
        d = StepDie(size=dice_size)
        return d.throw()

    def throw(self):
        """Throw the dice and set the thrown state on.
        """
        if self.thrown:
            return self.result
        adv_die_res = None
        if self.advantage:
            if self.attr < self.skill:  # A < B
                adv_die_res = self.value_to_dice(value=self.skill)
            else:
                adv_die_res = self.value_to_dice(value=self.attr)
        elif self.advantage is False:
            # then it’s a disavantage
            if self.attr > self.skill:
                self.skill = None
            else:
                self.attr = None
        attr_res = self.value_to_dice(value=self.attr)
        skill_res = self.value_to_dice(value=self.skill)
        if attr_res:
            self.result['attr'] = attr_res
        if skill_res:
            self.result['skill'] = skill_res
        if adv_die_res:
            self.result['adv_die'] = adv_die_res
        self.thrown = True
        return self.result

    def check_res_and_push(self, res, value, even_one_success=False):
        """Push the dice unless it already has two success or one
        success while even_one_success is set to False
        """
        if res[1] > 1:
            return res
        if res[1] == 1 and not even_one_success:
            return res
        return self.value_to_dice(value=value)

    def push(self, even_one_success=False):

        """Push all dice you can push, even if you got one success on one
        """
        if self.pushed:
            return self.pushed_res
        if 'attr' in self.result:
            self.pushed_res['attr'] = self.check_res_and_push(self.result['attr'], self.attr, even_one_success)
        if 'skill' in self.result:
            self.pushed_res['skill'] = self.check_res_and_push(self.result['skill'], self.skill, even_one_success)
        if 'adv_die' in self.result:
            if self.attr < self.skill:
                adv_die = self.skill
            else:
                adv_die = self.attr
            self.pushed_res['adv_die'] = self.check_res_and_push(self.result['adv_die'], adv_die, even_one_success)
        self.pushed = True
        return self.pushed_res
   
