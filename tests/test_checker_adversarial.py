"""Adversarial tests for independent certificate verification."""
import copy
import json
import unittest

from stopverify.checker import check_document, check_json

BASE = {
    "schema": "stopverify.bellman.v1",
    "distributions": [[["1", "1"]], [["0", "1/2"], ["2", "1/2"]]],
    "values": ["1", "1"],
    "policy": [[["1", True]], [["0", True], ["2", True]]],
}

class AdversarialCheckerTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(check_document(BASE)["verified"])
        self.assertEqual(check_document(BASE)["optimal_value"], "1")

    def test_without_policy(self):
        doc = copy.deepcopy(BASE)
        del doc["policy"]
        self.assertTrue(check_document(doc)["verified"])

    def test_mutations(self):
        edits = [
            ("schema", "invalid"),
            ("values", ["3/2", "1"]),
            ("values", ["1", "3/2"]),
            ("values", ["1"]),
            ("distributions", []),
            ("distributions", [[["1", "1/2"]], [["0", "1/2"], ["2", "1/2"]]]),
            ("distributions", [[["1", "1"]], [["0", "1/2"], ["0", "1/2"]]]),
            ("distributions", [[["1", "1"]], [["0", "-1/2"], ["2", "3/2"]]]),
            ("policy", [[["1", False]], [["0", True], ["2", True]]]),
            ("policy", [[["1", True]], [["0", False], ["2", True]]]),
            ("policy", [[["1", True]], [["0", True], ["2", False]]]),
            ("policy", [[["1", 1]], [["0", True], ["2", True]]]),
        ]
        for key, replacement in edits:
            with self.subTest(key=key, replacement=replacement):
                doc = copy.deepcopy(BASE)
                doc[key] = replacement
                self.assertFalse(check_document(doc)["verified"])

    def test_rational_strings(self):
        for invalid in ["1.0", "01", "1/-2", "1/0", "NaN", "Infinity", "1e3", " 1", "1 "]:
            with self.subTest(invalid=invalid):
                doc = copy.deepcopy(BASE)
                doc["values"][0] = invalid
                self.assertFalse(check_document(doc)["verified"])

    def test_malformed_json(self):
        for s in ["{", '{"x":NaN}', '{"x":Infinity}', '{"x":1.0}', "[]"]:
            with self.subTest(s=s):
                self.assertFalse(check_json(s)["verified"])

    def test_unexpected_field(self):
        doc = copy.deepcopy(BASE)
        doc["arbitrary"] = 7
        self.assertFalse(check_document(doc)["verified"])

    def test_limits(self):
        self.assertFalse(check_json("x" * 1_000_001)["verified"])
        doc = copy.deepcopy(BASE)
        doc["values"][0] = "9" * 201
        self.assertFalse(check_document(doc)["verified"])

    def test_negative_rewards(self):
        doc = {"schema": BASE["schema"], "distributions": [[["-3", "1"]], [["-2", "1"]]],
               "values": ["-2", "-2"], "policy": [[["-3", False]], [["-2", True]]]}
        self.assertTrue(check_document(doc)["verified"])

    def test_ties(self):
        doc = {"schema": BASE["schema"], "distributions": [[["1", "1"]], [["1", "1"]]],
               "values": ["1", "1"], "policy": [[["1", False]], [["1", True]]]}
        self.assertTrue(check_document(doc)["verified"])

if __name__ == "__main__":
    unittest.main()
