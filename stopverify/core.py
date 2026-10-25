"""Exact finite-horizon stopping and prophet calculations."""
from fractions import Fraction as F
from itertools import product


def q(x):
    if isinstance(x, float):
        raise TypeError('Floating-point input is forbidden; use strings or Fraction')
    return F(x)


def normalize(distributions):
    if not distributions:
        raise ValueError('At least one observation is required')
    result = []
    for dist in distributions:
        if not dist:
            raise ValueError('Empty distribution')
        d = {}
        for x, p in dist:
            x, p = q(x), q(p)
            if p < 0:
                raise ValueError('Negative probability')
            d[x] = d.get(x, F(0)) + p
        if sum(d.values(), F(0)) != 1:
            raise ValueError('Probabilities must sum to one')
        result.append(tuple(sorted((x,p) for x,p in d.items() if p)))
    return tuple(result)


def solve(distributions):
    ds = normalize(distributions)
    values = [F(0)] * len(ds)
    values[-1] = sum((x*p for x,p in ds[-1]), F(0))
    for i in range(len(ds)-2,-1,-1):
        values[i] = sum((p*max(x,values[i+1]) for x,p in ds[i]), F(0))
    return tuple(values)


def policy_value(distributions, decisions):
    """Independent forward probability propagation for a deterministic policy.

    decisions[i] maps each support value to True (stop) or False (continue).
    The last observation is mandatory.
    """
    ds = normalize(distributions)
    if len(decisions) != len(ds):
        raise ValueError('Incorrect policy length')
    alive, reward = F(1), F(0)
    for i, d in enumerate(ds):
        keys = {x for x,_ in d}
        if set(decisions[i]) != keys:
            raise ValueError('Missing or extra decisions')
        if i == len(ds)-1 and not all(decisions[i].values()):
            raise ValueError('Last observation must be accepted')
        stopping = sum((p*x for x,p in d if decisions[i][x]), F(0))
        continuing = sum((p for x,p in d if not decisions[i][x]), F(0))
        reward += alive * stopping
        alive *= continuing
    return reward


def threshold_policy(distributions, values):
    ds = normalize(distributions)
    if len(values) != len(ds):
        raise ValueError('Incorrect value vector length')
    return tuple({x: (i==len(ds)-1 or x>=values[i+1]) for x,p in d} for i,d in enumerate(ds))


def prophet(distributions):
    """Independent computation using the CDF of the maximum."""
    ds = normalize(distributions)
    support = sorted({x for d in ds for x,p in d})
    cdf = []
    for z in support:
        probability = F(1)
        for d in ds:
            probability *= sum((p for x,p in d if x <= z), F(0))
        cdf.append(probability)
    return support[0] + sum(((support[j]-support[j-1])*(1-cdf[j-1]) for j in range(1,len(support))), F(0))


def verify_certificate(distributions, values, decisions=None):
    """Check supplied Bellman identities directly; never invoke solve()."""
    ds = normalize(distributions)
    if len(values) != len(ds):
        return False, 'Incorrect number of Bellman values'
    try:
        v = tuple(q(x) for x in values)
    except (TypeError, ValueError, ZeroDivisionError) as e:
        return False, str(e)
    for i,d in enumerate(ds):
        expected = sum((p*(x if i==len(ds)-1 else max(x,v[i+1])) for x,p in d),F(0))
        if v[i] != expected:
            return False, f'Bellman identity fails at observation {i+1}: expected {expected}, received {v[i]}'
    if decisions is not None:
        try:
            actual = policy_value(ds, decisions)
        except (ValueError, TypeError) as e:
            return False, str(e)
        if actual != v[0]:
            return False, f'Policy is suboptimal: reward {actual}, optimal value {v[0]}'
    return True, 'Exact Bellman identities verified' + ('; policy reward verified' if decisions is not None else '')


def enumerate_optimum(distributions, max_policies=1000000):
    """Independent exhaustive policy enumeration, intended for small examples."""
    ds = normalize(distributions)
    sizes = [2**len(d) for d in ds[:-1]]
    total = 1
    for size in sizes:
        total *= size
    if total > max_policies:
        raise ValueError('Policy enumeration limit exceeded')
    best = None
    for masks in product(*(range(size) for size in sizes)):
        decisions = []
        for i,mask in enumerate(masks):
            decisions.append({x: bool(mask & (1<<j)) for j,(x,p) in enumerate(ds[i])})
        decisions.append({x: True for x,p in ds[-1]})
        score = policy_value(ds,decisions)
        if best is None or score > best:
            best = score
    if best is None:
        best = policy_value(ds,({x: True for x,p in ds[0]},))
    return best


def counterexample(distributions, constant):
    ds = normalize(distributions)
    c = q(constant)
    v, m = solve(ds)[0], prophet(ds)
    return {'optimal':str(v),'prophet':str(m),'constant':str(c),
            'gap':str(m-c*v),'violates':m>c*v}
