The main goal of this Python library is to propose an object to emulate
Year Zero Engine dice throwing.

# System supported:
- [X] Mutant: Year Zero
- [X] Forbidden Lands
- [X] Twilight 2000
- [X] Alien
- [X] Blade Runner

# Example
```
. my_py_venv/bin/activate
git clone https://github.com/nlegrand/yze.git
cd yze
python -m pip install -e .
python
Python 3.11.3 (main, Apr  8 2023, 02:16:51) [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from yze.dice import MutantDicePool
>>> d = MutantDicePool(attr=3, skill=2, gear=2)
>>> d.throw()
{'attr': [5, 6, 6], 'skill': [1, 4], 'gear': [6, 2]}
>>> d.push()
{'attr': [2, 6, 6], 'skill': [5, 2], 'gear': [6, 1]}
>>> from yze.dice import FBLDicePool
>>> fbl = FBLDicePool(attr=2, skill=1, artefact=12)
>>> fbl.throw()
{'attr': [2, 2], 'skill': [2], 'gear': [], 'artefact': (8, 2)}
>>> fbl.push()
{'attr': [2, 6], 'skill': [3], 'gear': [], 'artefact': (8, 2)}
>>> from yze.dice import AlienDicePool
>>> alien = AlienDicePool(pool=4, stress=1)
>>> alien.throw()
{'pool': [4, 1, 6, 1], 'stress': [2]}
>>> alien.push()
{'pool': [1, 3, 6, 2], 'stress': [1, 1]}
```

# Odds of pushing

Free League gives very general chances to get a succes when throwing
and pushing a dice pool according to it’s size. But how can we get
odds after the first roll is made? `mutant_odds_of_pushing` tries do
do exactly that. Here is the doc:

```
$ mutant_odds_of_pushing  --help           
usage: mutant_odds_of_pushing [-h] [-t THROWS] -a ATTRIBUTE_DICE [-s SKILL_DICE] [-g GEAR_DICE]

Once you get a result, what are your odds when pushing it? feed this command your results and see what is likely or not to happen

options:
  -h, --help            show this help message and exit
  -t THROWS, --throws THROWS
  -a ATTRIBUTE_DICE, --attribute_dice ATTRIBUTE_DICE
                        List your dice results eg: 253
  -s SKILL_DICE, --skill_dice SKILL_DICE
                        List your dice results eg: 45
  -g GEAR_DICE, --gear_dice GEAR_DICE
                        List your dice results eg: 32

Experimental probabilities made with pseudo random numbers. Maybie it’s not the best you can get :).
```
And here is an example:


```
$ mutant_odds_of_pushing -a 253 -s 45 -g 32
Throwing dice 100000 times !
Odds of having:
    -at least one success: 72.026 %
    -at least one attr botch: 42.091 %
    -at least one gear botch: 30.404 %
    - 1 successes: 39.356 %
    - 2 successes: 23.168 %
    - 3 successes: 7.759 %
    - 4 successes: 1.543 %
    - 5 successes: 0.192 %
    - 6 successes: 0.008 %
    - 1 attribute botchs: 34.628 %
    - 2 attribute botchs: 6.957 %
    - 3 attribute botchs: 0.506 %
    - 1 gear botchs: 27.686 %
    - 2 gear botchs: 2.718 %
```

Running multiple times produce different odds, but in the same order.

# Benchmark
You can also benchmark dice throw to see what are your chances to get
some successes or damage.

```
benchmark_mutant --throws 10000 --attribute 4 --skill 2 --gear 1
Throwing dice 10000 times !
    at least one success : 7243
    at least one pushed success : 9096
    at least one damage to attribute : 7245
    at least one damage to gear : 2767
{   'atleast_one': 7243,
    'atleast_one_attr_botch': 7245,
    'atleast_one_gear_botch': 2767,
    'atleast_one_pushed': 9096,
    'attribute_botched': {1: 4158, 2: 2404, 3: 622, 4: 61},
    'gear_botched': {1: 2767},
    'pushed_successes': {1: 2666, 2: 3304, 3: 2070, 4: 843, 5: 194, 6: 19},
    'successes': {1: 3895, 2: 2424, 3: 757, 4: 154, 5: 13}}
```

Yes I know, I can improve this output :). I'll do it!
