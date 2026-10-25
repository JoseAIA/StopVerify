import json
import unittest
from copy import deepcopy
from fractions import Fraction
from stopverify import create_certificate, check_document, check_json, solve, enumerate_optimum

class CheckerTests(unittest.TestCase):
    def test_roundtrip(self):
        examples=[[[('-3','1/2'),('-1','1/2')]], [[(1,1)],[(0,'1/2'),(2,'1/2')]], [[(-3,1)],[(-2,1)]], [[(1,1)],[(1,1)]]]
        for ds in examples:
            cert=create_certificate(ds)
            self.assertTrue(check_json(json.dumps(cert))['verified'])
            self.assertEqual(Fraction(check_document(cert)['optimal_value']),enumerate_optimum(ds))
    def test_tampering(self):
        cert=create_certificate([[(1,1)],[(0,'1/2'),(2,'1/2')]])
        for change in ('value','policy','probability','terminal','schema','duplicate'):
            bad=deepcopy(cert)
            if change=='value': bad['values'][0]='999'
            if change=='policy':
                bad=create_certificate([[(2,1)],[(0,'1/2'),(2,'1/2')]])
                bad['policy'][0][0][1]=False
            if change=='probability': bad['distributions'][1][0][1]='2/3'
            if change=='terminal': bad['policy'][1][0][1]=False
            if change=='schema': bad['schema']='unknown'
            if change=='duplicate': bad['distributions'][1].append(bad['distributions'][1][0])
            self.assertFalse(check_document(bad)['verified'],change)
    def test_no_floats(self):
        self.assertFalse(check_json('{"schema":"stopverify.bellman.v1","values":[1.0]}')['verified'])
        self.assertFalse(check_document({'schema':'stopverify.bellman.v1','distributions':[[['1',1.0]]],'values':['1']})['verified'])
    def test_policy_optional(self):
        cert=create_certificate([[(0,'1/2'),(2,'1/2')],[(1,1)]],include_policy=False)
        self.assertTrue(check_document(cert)['verified'])
    def test_independent_imports(self):
        import pathlib
        import stopverify.checker as checker
        source=pathlib.Path(checker.__file__).read_text()
        self.assertNotIn('from .core',source)
        self.assertNotIn('from .audit',source)
