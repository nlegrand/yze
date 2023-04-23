The main goal of this Python library is to propose an object to emulate
Year Zero Engine dice throwing.

# System supported:
- [X] Mutant: Year Zero
- [X] Forbidden Lands
- [ ] Twilight 2000
- [X] Alien
- [ ] Blade Runner

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

# Benchmark
You can also benchmark dice throw to see what are your chances to get
some successes or damage.

```
benchmark_mutant --throw 10000 --attribute 4 --skill 2 --gear 1
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
