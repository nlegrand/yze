The main goal of this Python library is to propose an object to emulate
Year Zero Engine dice throwing.

# What is it about?

The Year Zero Engine is a very nice Roleplaying Game system created by
the terrific Tomas Härenstam at [Free League
Publishing](https://freeleaguepublishing.com/). You can check the
[SRD](https://freeleaguepublishing.com/en/free-tabletop-licenses/) to
see how it is done or [the
games](https://freeleaguepublishing.com/en/store/) directly.

This Python module is unofficial and not affiliated with Free
League. I've made it just for fun.

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
$ benchmark_mutant  -a 4 -s 2 -g 2
Throwing dice pool (attribute: 4, skill: 2, gear: 2) 100000 times !
at least one success: 76.791 %
at least on pushed succes: 93.235 %
at least one damage to attribute: 73.079 %
at least one damage to gear: 47.882 %
Successes on first roll:
    chances to get 1: 37.343 %
    chances to get 2: 25.997 %
    chances to get 3: 10.273 %
    chances to get 4: 2.718 %
    chances to get 5: 0.422 %
    chances to get 6: 0.036 %
    chances to get 7: 0.002 %
Successes on pushed roll:
    chances to get 1: 21.921 %
    chances to get 2: 30.324 %
    chances to get 3: 24.232 %
    chances to get 4: 11.968 %
    chances to get 5: 3.886 %
    chances to get 6: 0.813 %
    chances to get 7: 0.088 %
    chances to get 8: 0.003 %
Attribute damage:
    chances to get 1: 41.93 %
    chances to get 2: 24.337 %
    chances to get 3: 6.247 %
    chances to get 4: 0.565 %
Gear damage:
    chances to get 1: 40.233 %
    chances to get 2: 7.649 %

```

