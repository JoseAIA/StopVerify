import unittest
from fractions import Fraction as F
from itertools import product
from stopverify import *

class TestStopVerify(unittest.TestCase):
    def test_one_negative(self):
        d=[[('-3','1/2'),('-1','1/2')]]
        self.assertEqual(solve(d),(F(-2),))
        self.assertEqual(prophet(d),F(-2))
        self.assertEqual(enumerate_optimum(d),F(-2))
    def test_counterexample(self):
        d=[[(1,1)],[(0,'1/2'),(2,'1/2')]]
        self.assertEqual(solve(d)[0],F(1))
        self.assertEqual(prophet(d),F(3,2))
        self.assertTrue(counterexample(d,'7/5')['violates'])
    def test_ties(self):
        d=[[(1,1)],[(1,1)]]
        v=solve(d)
        self.assertTrue(verify_certificate(d,v,threshold_policy(d,v))[0])
        self.assertTrue(verify_certificate(d,v,({F(1):False},{F(1):True}))[0])
    def test_reject_wrong(self):
        d=[[(0,'1/2'),(2,'1/2')],[(1,1)]]
        self.assertFalse(verify_certificate(d,(F(0),F(1)))[0])
        self.assertFalse(verify_certificate(d,solve(d),({F(0):True,F(2):True},{F(1):True}))[0])
    def test_input_validation(self):
        for d in ([],[[]],[[(1,'1/2')]],[[(1,-1),(2,2)]],[[(1,0)]]):
            with self.assertRaises(ValueError): normalize(d)
        with self.assertRaises(TypeError): normalize([[(1.0,1)]])
    def test_exhaustive_grid(self):
        distributions = [([(a,'1/2'),(b,'1/2')]) for a,b in product(range(-2,3),repeat=2)]
        for n in (1,2,3):
            for ds in product(distributions,repeat=n):
                v=solve(ds)
                self.assertEqual(v[0],enumerate_optimum(ds))
                self.assertTrue(verify_certificate(ds,v,threshold_policy(ds,v))[0])
                self.assertGreaterEqual(prophet(ds),v[0])
                if n==3 and ds[0]!=distributions[0]:
                    break
if __name__=='__main__': unittest.main()
