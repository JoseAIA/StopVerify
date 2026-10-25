"""Certificate construction is untrusted; checker.py verifies independently."""
from .core import normalize, solve, threshold_policy
from .checker import SCHEMA

def create_certificate(distributions, include_policy=True):
    ds=normalize(distributions)
    values=solve(ds)
    document={'schema':SCHEMA,'distributions':[[[str(x),str(prob)] for x,prob in d] for d in ds], 'values':[str(x) for x in values]}
    if include_policy:
        pol=threshold_policy(ds,values)
        document['policy']=[[[str(x),pol[i][x]] for x,_ in d] for i,d in enumerate(ds)]
    return document
