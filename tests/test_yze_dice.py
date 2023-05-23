import unittest

import yze.dice


class TestYZEDice(unittest.TestCase):
    def test_is_int(self):
        """SimpleDie should return an int
        """
        d = yze.dice.SimpleDie()
        self.assertTrue(isinstance(d.throw(), int))

    def test_is_tuple(self):
        """ArtefactDie and StepDie should return a tuple of two int
        """
        ad = yze.dice.ArtefactDie()
        res = ad.throw()
        self.assertTrue(isinstance(res, tuple))
        self.assertEqual(len(res), 2)
        self.assertTrue(isinstance(res[0], int))
        self.assertTrue(isinstance(res[1], int))
        sd = yze.dice.StepDie()
        sres = sd.throw()
        self.assertTrue(isinstance(sres, tuple))
        self.assertEqual(len(sres), 2)
        self.assertTrue(isinstance(sres[0], int))
        self.assertTrue(isinstance(sres[1], int))

    def test_location(self):
        """Hit Location Die return Leg, Torso, Arm or Head.
        """
        hld = yze.dice.HitLocationDie()

        self.assertEqual(hld.die_size, 6)
        leg = [x for x in hld.hit_location if x == "Leg"]
        self.assertEqual(len(leg), 1)
        torso = [x for x in hld.hit_location if x == "Torso"]
        self.assertEqual(len(torso), 3)
        arm = [x for x in hld.hit_location if x == "Arm"]
        self.assertEqual(len(arm), 1)
        head = [x for x in hld.hit_location if x == "Head"]
        self.assertEqual(len(head), 1)

        location = hld.throw()
        self.assertTrue(location, str)
        hit_locations = ["Leg", "Torso", "Arm", "Head"]
        test_location = [x for x in hit_locations if x == location]
        self.assertEqual(len(test_location), 1)

    def test_state_mutant(self):
        """MutantDicePool have state, thrown and pushed.
        """
        mdp = yze.dice.MutantDicePool()
        self.assertFalse(mdp.thrown)
        self.assertFalse(mdp.pushed)
        mdp.throw()
        self.assertTrue(mdp.thrown)
        mdp.push()
        self.assertTrue(mdp.pushed)

    def test_state_fbl(self):
        """FBLDicePool have state, thrown and pushed.
        """
        fbl = yze.dice.FBLDicePool()
        self.assertFalse(fbl.thrown)
        self.assertFalse(fbl.pushed)
        fbl.throw()
        self.assertTrue(fbl.thrown)
        fbl.push()
        self.assertTrue(fbl.pushed)

    def test_state_alien(self):
        """AlienDicePool have state, thrown, pushed and multipushed.
        """
        adp = yze.dice.AlienDicePool()
        self.assertFalse(adp.thrown)
        self.assertFalse(adp.pushed)
        self.assertFalse(adp.multipushed)
        adp.throw()
        self.assertTrue(adp.thrown)
        adp.push()
        self.assertTrue(adp.pushed)
        adp.multipush()
        self.assertTrue(adp.multipushed)



if __name__ == '__main__':
    unittest.main()
