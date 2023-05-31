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
import logging, sys, os

DEBUG=os.getenv('DEBUG')
loglevel = logging.INFO
if DEBUG:
    loglevel = logging.DEBUG
logging.basicConfig(stream=sys.stderr, level=loglevel)


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
    
    #print(f'Throwing dice pool (attribute: {attribute}, skill: {skill}, gear: {gear}) {throws} times !')
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


def complete_benchmark():
    """In dev yet, will launch multiple multiple_throws so as to try
    to have almost exhaustive benchmarks.

    """
    pass
def print_result(result_name, result, throws):
    """Pretty print result to terminal
    """
    print (f'{result_name}: {result * 100 / throws} %')

def print_result_list(throws):
    """Pretty print the full result list
    """
    attr = 1
    skill = 0
    gear = 0
    while attr < 6:
        while skill < 6:
            while gear < 3:
                results = multiple_throws(throws, attr, skill, gear)
                print(f"{attr}\t{skill}\t{gear}\t{results['atleast_one'] * 100 / throws} %\t{results['atleast_one_pushed'] * 100 / throws} %")
                gear += 1
            skill += 1
            gear = 0
        attr += 1
        skill = 0


def main():
    """Fetch args from the commandline and proceed.
    """
    parser = argparse.ArgumentParser(
                        prog='benchmark_mutant',
                        description='make a lot of YZE rolls so as to have an idea of chances of success',
                        epilog='')

    parser.add_argument('-t', '--throws', default=100000)      # option that takes a value
    parser.add_argument('-a', '--attribute', default=1)
    parser.add_argument('-s', '--skill', default=0)
    parser.add_argument('-g', '--gear', default=0)
    parser.add_argument('-c', '--complete', action='store_true')

    args = parser.parse_args()
    throws = int(args.throws)

    if args.complete:
        print_result_list(throws)
    else:
        results = multiple_throws(throws, args.attribute, args.skill, args.gear)
        print_result('at least one success', results['atleast_one'], throws)
        print_result('at least on pushed succes', results['atleast_one_pushed'], throws)
        print_result('at least one damage to attribute', results['atleast_one_attr_botch'], throws)
        print_result('at least one damage to gear', results['atleast_one_gear_botch'], throws)
        print_result_list('Successes on first roll', results['successes'], throws)
        print_result_list('Successes on pushed roll', results['pushed_successes'], throws)
        print_result_list('Attribute damage', results['attribute_botched'], throws)
        print_result_list('Gear damage', results['gear_botched'], throws)
        logging.debug(results)

if __name__ == "__main__":
    main()
