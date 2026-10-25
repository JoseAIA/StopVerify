"""Independent, exact rational Bellman certificate checker.

No solver imports. This checks a finite-instance claim, not a universal theorem.
"""
from fractions import Fraction
import json
import re

SCHEMA = "stopverify.bellman.v1"
_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
MAX_DOCUMENT_CHARS = 1_000_000
MAX_HORIZON = 1000
MAX_OUTCOMES = 100_000
MAX_RATIONAL_CHARS = 200

def _r(value):
    if type(value) is not str or len(value) > MAX_RATIONAL_CHARS or not _RATIONAL.fullmatch(value):
        raise ValueError("Expected canonical rational string (integer or numerator/positive denominator)")
    return Fraction(value)

def _reject_constant(value):
    raise ValueError("Nonstandard JSON numeric constant is forbidden")

def check_document(doc):
    """Return a structured report; verified=True certifies the supplied instance."""
    try:
        if type(doc) is not dict or doc.get("schema") != SCHEMA:
            raise ValueError("Unsupported certificate schema")
        if set(doc) - {"schema", "distributions", "values", "policy"}:
            raise ValueError("Unexpected certificate fields")
        distributions = doc["distributions"]
        values = doc["values"]
        if type(distributions) is not list or not (1 <= len(distributions) <= MAX_HORIZON):
            raise ValueError("Invalid horizon")
        if type(values) is not list or len(values) != len(distributions):
            raise ValueError("Incorrect value vector length")
        ds = []
        count = 0
        for dist in distributions:
            if type(dist) is not list or not dist:
                raise ValueError("Empty or malformed distribution")
            masses = {}
            for pair in dist:
                if type(pair) is not list or len(pair) != 2:
                    raise ValueError("Malformed outcome-probability pair")
                x, prob = map(_r, pair)
                if prob <= 0:
                    raise ValueError("Probabilities must be strictly positive")
                if x in masses:
                    raise ValueError("Duplicate support value")
                masses[x] = prob
                count += 1
                if count > MAX_OUTCOMES:
                    raise ValueError("Too many outcomes")
            if sum(masses.values(), Fraction(0)) != 1:
                raise ValueError("Probabilities do not sum to one")
            ds.append(masses)
        v = list(map(_r, values))
        n = len(ds)
        for i in range(n - 1, -1, -1):
            rhs = sum((prob * (x if i == n - 1 else max(x, v[i + 1]))
                       for x, prob in ds[i].items()), Fraction(0))
            if v[i] != rhs:
                raise ValueError(f"Bellman identity fails at observation {i + 1}: expected {rhs}, received {v[i]}")
        if "policy" in doc:
            policy = doc["policy"]
            if type(policy) is not list or len(policy) != n:
                raise ValueError("Incorrect policy length")
            alive = Fraction(1)
            earned = Fraction(0)
            for i, decisions in enumerate(policy):
                if type(decisions) is not list:
                    raise ValueError("Malformed policy")
                actions = {}
                for entry in decisions:
                    if type(entry) is not list or len(entry) != 2 or type(entry[1]) is not bool:
                        raise ValueError("Malformed policy entry")
                    x = _r(entry[0])
                    if x in actions:
                        raise ValueError("Duplicate policy outcome")
                    actions[x] = entry[1]
                if actions.keys() != ds[i].keys():
                    raise ValueError("Policy support mismatch")
                if i == n - 1 and not all(actions.values()):
                    raise ValueError("Terminal stopping is mandatory")
                earned += alive * sum((x * prob for x, prob in ds[i].items() if actions[x]), Fraction(0))
                alive *= sum((prob for x, prob in ds[i].items() if not actions[x]), Fraction(0))
            if earned != v[0]:
                raise ValueError(f"Policy is not optimal: reward {earned}, optimal {v[0]}")
        return {"verified": True, "optimal_value": str(v[0]),
                "scope": "finite instance only; not a universal theorem"}
    except (ValueError, TypeError, KeyError, AttributeError, OverflowError, ZeroDivisionError) as exc:
        return {"verified": False, "reason": str(exc)}

def check_json(text):
    if type(text) is not str or len(text) > MAX_DOCUMENT_CHARS:
        return {"verified": False, "reason": "JSON document must be a string within size limit"}
    try:
        doc = json.loads(text, parse_float=lambda _: (_ for _ in ()).throw(ValueError("JSON floats forbidden")),
                         parse_constant=_reject_constant)
        return check_document(doc)
    except (ValueError, TypeError, RecursionError, OverflowError) as exc:
        return {"verified": False, "reason": str(exc)}
