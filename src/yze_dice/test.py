from yze_dice import DicePoolMutant


results = {'successes': 0, 'pushed_successes': 0, 'attribute_botched': 0, 'gear_botched': 0}

for i in range(10000):
    d = DicePoolMutant(attr=4, skill=2, gear=1)
    res = d.throw()
    pushed_res = d.push()
    successes = [x for x in d.result['attr'] + d.result['skill'] + d.result['gear'] if x == 6]
    pushed_successes = [x for x in d.pushed_res['attr'] + d.pushed_res['skill'] + d.pushed_res['gear'] if x == 6]
    attribute_botched = [x for x in d.pushed_res['attr'] if x == 1]
    gear_botched = [x for x in d.pushed_res['gear'] if x == 1]
    results['successes'] += len(successes)
    results['pushed_successes'] += len(pushed_successes)
    results['attribute_botched'] += len(attribute_botched)
    results['gear_botched'] += len(gear_botched)

print(f'succès : {(results["successes"] * 100) / (10000 * 7)}')
print(f'succès poussés : {(results["pushed_successes"] * 100) / (10000 * 7)}')
print(f'rattages attr : {(results["attribute_botched"] * 100) / (10000 * 4)}')
print(f'rattages mat : {(results["gear_botched"] * 100) / (10000 * 1)}')

    
print(results)
    
