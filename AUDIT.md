# StopVerify v0.2.1 — Internal audit

The checker is implemented in `stopverify/checker.py` and does not import the solver, shared normalizer, or certificate generator. It parses rational strings, checks distribution validity, verifies all Bellman equalities, and independently evaluates a supplied policy using forward probability propagation.

Limitations: internal audit only; no external referee validation; checker and generator share the mathematical specification; finite examples do not prove universal theorems. GitHub CI is configured but has not yet run on GitHub. Performance, security, and unbounded input-size behavior have not been externally assessed.

Do not describe the software as independently certified. The counterexample helper in `audit.py` remains a convenience routine; certificates are the preferred verification interface.
