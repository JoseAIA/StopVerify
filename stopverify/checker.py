"""Standalone, standard-library-only rational certificate checker.

No imports from solver, core, or audit. Untrusted JSON is parsed from scratch.
"""
from fractions import Fraction
import json

SCHEMA = 'stopverify.bellman.v1'

def _r(value):
    if not isinstance(value, str):
        raise ValueError('Rational values must be strings')
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('Invalid rational string') from exc

def check_document(doc):
    """Return a verification report. Only successful reports certify optimality."""
    try:
        if not isinstance(doc, dict) or doc.get('schema') != SCHEMA:
            raise ValueError('Unsupported certificate schema')
        distributions = doc['distributions']
        values = doc['values']
        if not isinstance(distributions, list) or not distributions:
            raise ValueError('Expected nonempty distribution list')
        if not isinstance(values, list) or len(values) != len(distributions):
            raise ValueError('Incorrect value vector length')
        ds=[]
        for dist in distributions:
            if not isinstance(dist, list) or not dist:
                raise ValueError('Empty or malformed distribution')
            masses={}
            for pair in dist:
                if not isinstance(pair, list) or len(pair)!=2:
                    raise ValueError('Malformed outcome-probability pair')
                x,prob=map(_r,pair)
                if prob<=0:
                    raise ValueError('Probabilities must be strictly positive')
                if x in masses:
                    raise ValueError('Duplicate support value')
                masses[x]=prob
            if sum(masses.values(),Fraction(0)) != 1:
                raise ValueError('Probabilities do not sum to one')
            ds.append(masses)
        v=list(map(_r,values))
        n=len(ds)
        for i in range(n-1,-1,-1):
            rhs=sum((prob*(x if i==n-1 else max(x,v[i+1])) for x,prob in ds[i].items()),Fraction(0))
            if v[i]!=rhs:
                raise ValueError(f'Bellman identity fails at observation {i+1}: expected {rhs}, received {v[i]}')
        if 'policy' in doc:
            policy=doc['policy']
            if not isinstance(policy,list) or len(policy)!=n:
                raise ValueError('Incorrect policy length')
            alive=Fraction(1)
            earned=Fraction(0)
            for i,decisions in enumerate(policy):
                if not isinstance(decisions,list):
                    raise ValueError('Malformed policy')
                actions={}
                for entry in decisions:
                    if not isinstance(entry,list) or len(entry)!=2 or type(entry[1]) is not bool:
                        raise ValueError('Malformed policy entry')
                    x=_r(entry[0])
                    if x in actions:
                        raise ValueError('Duplicate policy outcome')
                    actions[x]=entry[1]
                if actions.keys()!=ds[i].keys():
                    raise ValueError('Policy support mismatch')
                if i==n-1 and not all(actions.values()):
                    raise ValueError('Terminal stopping is mandatory')
                earned+=alive*sum((x*prob for x,prob in ds[i].items() if actions[x]),Fraction(0))
                alive*=sum((prob for x,prob in ds[i].items() if not actions[x]),Fraction(0))
            if earned!=v[0]:
                raise ValueError(f'Policy is not optimal: reward {earned}, optimal {v[0]}')
        return {'verified':True,'optimal_value':str(v[0]),'scope':'finite instance only; not a universal theorem'}
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return {'verified':False,'reason':str(exc)}

def check_json(text):
    try:
        return check_document(json.loads(text,parse_float=lambda _: (_ for _ in ()).throw(ValueError('JSON floats forbidden'))))
    except (ValueError, TypeError) as exc:
        return {'verified':False,'reason':str(exc)}
