"""Small independent reference routines based on full outcome-path enumeration."""
from fractions import Fraction
from itertools import product
from .core import normalize, q


def path_prophet(distributions, max_paths=1000000):
    """Compute E[max(X_i)] by enumerating full paths, not using CDF formulas."""
    ds = normalize(distributions)
    count = 1
    for d in ds:
        count *= len(d)
    if count > max_paths:
        raise ValueError('Path enumeration limit exceeded')
    result = Fraction(0)
    for path in product(*ds):
        prob = Fraction(1)
        for _, p in path:
            prob *= p
        result += prob * max(x for x, _ in path)
    return result


def path_policy_value(distributions, decisions, max_paths=1000000):
    """Evaluate a policy by enumerating full paths, independent of forward propagation."""
    ds = normalize(distributions)
    if len(decisions) != len(ds):
        raise ValueError('Incorrect policy length')
    for i, d in enumerate(ds):
        if set(decisions[i]) != {x for x, _ in d}:
            raise ValueError('Policy has missing or extra decisions')
    if not all(decisions[-1].values()):
        raise ValueError('Terminal observation must be accepted')
    count = 1
    for d in ds:
        count *= len(d)
    if count > max_paths:
        raise ValueError('Path enumeration limit exceeded')
    total = Fraction(0)
    for path in product(*ds):
        probability = Fraction(1)
        for _, p in path:
            probability *= p
        reward = path[-1][0]
        for i, (x, _) in enumerate(path):
            if decisions[i][x]:
                reward = x
                break
        total += probability * reward
    return total


def check_prophet_bound(distributions, constant, claimed=True, max_paths=1000000):
    """Produce exact, independently recomputed instance witness (not a universal proof)."""
    from .core import solve, prophet, threshold_policy, policy_value
    ds = normalize(distributions)
    c = q(constant)
    values = solve(ds)
    decisions = threshold_policy(ds, values)
    if path_policy_value(ds, decisions, max_paths) != policy_value(ds, decisions):
        raise AssertionError('Independent policy evaluators disagree')
    m = prophet(ds)
    if path_prophet(ds, max_paths) != m:
        raise AssertionError('Independent prophet evaluators disagree')
    gap = m - c * values[0]
    return {'instance': [[[str(x), str(p)] for x, p in d] for d in ds],
            'optimal': str(values[0]), 'prophet': str(m), 'constant': str(c),
            'gap': str(gap), 'violates': gap > 0,
            'scope': 'exact finite-instance witness; not a universal proof'}
