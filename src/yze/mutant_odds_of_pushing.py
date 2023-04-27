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

def multiple_throws(attribute, skill, gear, throws=100000):
    """Throw dice <throws> times, store results in <results>, return
    results.
    """
    results = {
        'atleast_one_pushed': 0,
        'atleast_one_attr_botch': 0,
        'atleast_one_gear_botch': 0,
        'pushed_successes': {},
        'attribute_botched': {},
        'gear_botched': {},
    }
    
    print(f'Throwing dice {throws} times !')
    for i in range(int(throws)):
        d = MutantDicePool(attr=len(attribute), skill=len(skill), gear=len(gear))
        d.thrown = True
        d.result = {'attr': attribute, 'skill': skill, 'gear': gear}
        pushed_res = d.push()
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

def unpack(args):
    unpacked = []
    for att in args:
        att = int(att)
        if (att == 0):
            next;
        elif ( 1 <= att <= 6 ):
            unpacked.append(att)
        else:
            raise ValueError(f"got {att} should has been int between 0 and 6")
    return unpacked

def main():
    """Fetch args from the commandline and proceed.
    """
    parser = argparse.ArgumentParser(
                        prog='mutant_odds_of_pushing',
                        description="""Once you get a result, what are your odds when pushing it?
                        feed this command your results and see what is likely or not to happen""",
                        epilog="""Experimental probabilities made with pseudo random numbers.
                        Maybie it’s not the best you can get :).""")

    parser.add_argument('-t', '--throws', default=100000)      # option that takes a value
    parser.add_argument('-a', '--attribute_dice',
                        help="List your dice results eg: 253",
                        required=True)
    parser.add_argument('-s', '--skill_dice',
                        default=0,
                        help="List your dice results eg: 45")
    parser.add_argument('-g', '--gear_dice',
                        default=0,
                        help="List your dice results eg: 32")

    args = parser.parse_args()

    attribute_res = unpack(args.attribute_dice)
    skill_res = unpack(args.skill_dice)
    gear_res = unpack(args.gear_dice)

    throws = int(args.throws)

    results = multiple_throws(attribute_res, skill_res, gear_res,throws=throws)

    print ("Odds of having:")
    print (f"    -at least one success: {results['atleast_one_pushed'] * 100 / throws} %")
    print (f"    -at least one attr botch: {results['atleast_one_attr_botch'] * 100 / throws} %")
    print (f"    -at least one gear botch: {results['atleast_one_gear_botch'] * 100 / throws} %")
    for key in sorted(results['pushed_successes']):
        print (f"    - {key} successes: {results['pushed_successes'][key] * 100 / throws} %")
    for key in sorted(results['attribute_botched']):
        print (f"    - {key} attribute botchs: {results['attribute_botched'][key] * 100 / throws} %")
    for key in sorted(results['gear_botched']):
        print (f"    - {key} gear botchs: {results['gear_botched'][key] * 100 / throws} %")


if __name__ == "__main__":
    main()
