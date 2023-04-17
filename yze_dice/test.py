import unittest

import yze_dice


class TestYZEDice(unittest.TestCase):
    def test_is_int(self):
        d = yze_dice.Dice()
        self.assertTrue(isinstance(d.throw(), int))

    def test_is_tuple(self):
        ad = yze_dice.ArtefactDice()
        res = ad.throw()
        self.assertTrue(isinstance(res, tuple))
        self.assertEqual(len(res), 2)
        self.assertTrue(isinstance(res[0], int))
        self.assertTrue(isinstance(res[1], int))
        sd = yze_dice.StepDice()
        sres = sd.throw()
        self.assertTrue(isinstance(sres, tuple))
        self.assertEqual(len(sres), 2)
        self.assertTrue(isinstance(sres[0], int))
        self.assertTrue(isinstance(sres[1], int))

    def test_state(self):
        mdp = yze_dice.MutantDicePool()
        self.assertFalse(mdp.thrown)
        self.assertFalse(mdp.pushed)
        mdp.throw()
        self.assertTrue(mdp.thrown)
        mdp.push()
        self.assertTrue(mdp.pushed)
        fbl = yze_dice.FBLDicePool()
        self.assertFalse(fbl.thrown)
        self.assertFalse(fbl.pushed)
        fbl.throw()
        self.assertTrue(fbl.thrown)
        fbl.push()
        self.assertTrue(fbl.pushed)


if __name__ == '__main__':
    unittest.main()
