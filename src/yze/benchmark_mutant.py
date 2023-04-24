#!/usr/bin/env python3

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

from yze.dice import MutantDicePool
import argparse
import pprint

def multiple_throws(throws=10000, attribute=1, skill=0, gear=0):
    """Throw dice <throws> times, store results in <results>, return
    results.
    """
    results = {
        'atleast_one': 0,
        'atleast_one_pushed': 0,
        'atleast_one_attr_botch': 0,
        'atleast_one_gear_botch': 0,
        'successes': {},
        'pushed_successes': {},
        'attribute_botched': {},
        'gear_botched': {},
    }
    
    print(f'Throwing dice {throws} times !')
    for i in range(int(throws)):
        d = MutantDicePool(attr=int(attribute), skill=int(skill), gear=int(gear))
        res = d.throw()
        pushed_res = d.push()
        successes = [x for x in d.result['attr'] + d.result['skill'] + d.result['gear'] if x == 6]
        if len(successes) > 0:
            results['atleast_one'] += 1
            if len(successes) not in results['successes']:
                results['successes'][len(successes)] = 1
            else:
                results['successes'][len(successes)] += 1
        pushed_successes = [x for x in d.pushed_res['attr'] + d.pushed_res['skill'] + d.pushed_res['gear'] if x == 6]
        if len(pushed_successes) > 0:
            results['atleast_one_pushed'] += 1
            if len(pushed_successes) not in results['pushed_successes']:
                results['pushed_successes'][len(pushed_successes)] = 1
            else:
                results['pushed_successes'][len(pushed_successes)] += 1
        attribute_botched = [x for x in d.pushed_res['attr'] if x == 1]
        if len(attribute_botched) > 0:
            results['atleast_one_attr_botch'] += 1
            if len(attribute_botched) not in results['attribute_botched']:
                results['attribute_botched'][len(attribute_botched)] = 1
            else:
                results['attribute_botched'][len(attribute_botched)] += 1
        gear_botched = [x for x in d.pushed_res['gear'] if x == 1]
        if len(gear_botched) > 0:
            results['atleast_one_gear_botch'] += 1
            if len(gear_botched) not in results['gear_botched']:
                results['gear_botched'][len(gear_botched)] = 1
            else:
                results['gear_botched'][len(gear_botched)] += 1
    return results

def main():
    """Fetch args from the commandline and proceed.
    """
    parser = argparse.ArgumentParser(
                        prog='benchmark_mutant',
                        description='make a lot of YZE rolls so as to have an idea of chances of success',
                        epilog='')

    parser.add_argument('-t', '--throws', default=10000)      # option that takes a value
    parser.add_argument('-a', '--attribute', default=1)
    parser.add_argument('-s', '--skill', default=0)
    parser.add_argument('-g', '--gear', default=0)

    args = parser.parse_args()

    results = multiple_throws(args.throws, args.attribute, args.skill, args.gear)

    print (f'    at least one success : {results["atleast_one"]}')
    print (f'    at least one pushed success : {results["atleast_one_pushed"]}')
    print (f'    at least one damage to attribute : {results["atleast_one_attr_botch"]}')
    print (f'    at least one damage to gear : {results["atleast_one_gear_botch"]}')


    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(results)

if __name__ == "__main__":
    main()
