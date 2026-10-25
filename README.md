# StopVerify 0.2.1 (research preview)

Exact finite-horizon optimal stopping and prophet comparisons for **independent, finite-support, rational-valued** observations. No floating-point inputs. The terminal observation is mandatory even when negative. Ties allow either optimal action.

## Research need

StopVerify is intended for mathematicians and referees who need reproducible, exact **finite-instance** checks of optimal stopping policies and proposed prophet bounds. It does not prove universal inequalities from finite experiments. General-purpose probabilistic model checkers (PRISM, Storm) already solve related finite-state problems; StopVerify focuses on a compact probability-oriented interface, rational witnesses, and independently implemented audit routines.

## Install and test

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Reproducible example

```python
from stopverify import solve, prophet, threshold_policy, verify_certificate
from stopverify.audit import check_prophet_bound
D = [[(1,1)],[(0,'1/2'),(2,'1/2')]]
v = solve(D)
assert verify_certificate(D,v,threshold_policy(D,v))[0]
assert str(prophet(D)) == '3/2'
w = check_prophet_bound(D,'7/5')
assert w['gap'] == '1/10' and w['violates']
print(w)
```

`check_prophet_bound` independently compares CDF and full-path prophet calculations, and forward and full-path policy evaluations. It does not independently reproduce the optimality proof: Bellman identities must be checked with `verify_certificate`.

## Scope and limitations

- Only independent finite-support rational observations; forced stop at final observation.
- The full-path audit is exponential and capped at 1,000,000 paths by default.
- No secretary relative-rank model, continuous distributions, or proof of universal bounds yet.
- A certificate checked with the same software is not a formal proof-assistant verification.
- Research prototype: external validation and demonstrated adoption are pending.

See [mathematical specification](docs/MATHEMATICS.md), [audit](AUDIT.md), [contributing](CONTRIBUTING.md), and [roadmap](ROADMAP.md).

## Independent certificates (research preview)

```python
import json
from stopverify import create_certificate, check_json
instance = [[(1,1)],[(0,'1/2'),(2,'1/2')]]
certificate = create_certificate(instance)
assert check_json(json.dumps(certificate))['verified']
```

See [certificate specification](docs/CERTIFICATES.md). This is experimental research software, not a universal theorem prover or an externally certified system.

## Development and generative-AI assistance

StopVerify was initiated and is mathematically directed by José Á. Islas. OpenAI ChatGPT has substantially assisted with code implementation, documentation, tests, and internal review. The maintainer is responsible for independently understanding and validating the mathematics and software, and for all scientific claims. Automated tests and AI-assisted audits do not replace external review.
