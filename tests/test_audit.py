import unittest
from fractions import Fraction as F
from itertools import product
from stopverify import solve, prophet, policy_value, threshold_policy
from stopverify.audit import path_prophet, path_policy_value, check_prophet_bound

class IndependentAudit(unittest.TestCase):
    def test_full_small_grid(self):
        ds = [[(a,'1/2'),(b,'1/2')] for a,b in product(range(-2,3), repeat=2)]
        for n in (1,2,3):
            for sample in product(ds, repeat=n):
                vals = solve(sample)
                pol = threshold_policy(sample, vals)
                self.assertEqual(path_prophet(sample), prophet(sample))
                self.assertEqual(path_policy_value(sample, pol), policy_value(sample, pol))
                self.assertEqual(path_policy_value(sample, pol), vals[0])
                if n == 3 and sample[0] != ds[0]:
                    break
    def test_exact_violation(self):
        witness = check_prophet_bound([[(1,1)],[(0,'1/2'),(2,'1/2')]],'7/5')
        self.assertTrue(witness['violates'])
        self.assertEqual(witness['gap'],'1/10')
    def test_reject_invalid_policy(self):
        with self.assertRaises(ValueError):
            path_policy_value([[(0,1)]], [{F(0):False}])
    def test_negative_max(self):
        d = [[(-3,1)],[(-2,1)]]
        self.assertEqual(path_prophet(d), F(-2))
if __name__ == '__main__': unittest.main()
