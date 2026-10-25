# Bellman certificate format (v1)

A certificate is JSON with `schema`, `distributions`, `values`, and optionally `policy`. All rational values and probabilities **must be strings**, e.g. `"-3/2"`. Distributions are lists of `[outcome, probability]`, with strictly positive masses totaling one and distinct outcomes. `values[i]` is the optimal expected reward starting at observation i (0-indexed in JSON). A policy is a list of `[outcome, boolean_stop]` decisions for each observation. Terminal stopping is mandatory.

A successful check proves the stated finite-instance optimal value by backward induction; if policy is supplied, it additionally proves its optimality. It does not prove a universal prophet inequality. The independent checker imports neither the solver nor the certificate generator. This is source-level separation, not a formal proof of the software's implementation correctness.

Example:

```python
import json
from stopverify import create_certificate, check_json
doc = create_certificate([[(1,1)],[(0,'1/2'),(2,'1/2')]])
print(json.dumps(doc, indent=2))
print(check_json(json.dumps(doc)))
```
