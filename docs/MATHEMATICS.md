# Mathematical specification

Let X_1,...,X_n be independent rational-valued finite-support random variables with rational probabilities. The decision maker observes X_i, may stop and receive X_i, or continue; stopping at n is mandatory.

Define c_n=E[X_n], and for i<n, c_i=E[max(X_i,c_{i+1})]. Then c_1 is the optimal stopping value. A policy stopping at i<n when X_i>=c_{i+1}, and necessarily at n, is optimal. Proof: backward induction; conditional on X_i=x, stopping yields x and continuation yields c_{i+1} by independence. Hence the better choice yields max(x,c_{i+1}). All expressions are rational.

A certificate consists of the exact input distributions, candidate rational c_i, and optionally policy decisions on every positive-probability support point. A checker verifies the Bellman identities and the policy's exact expected reward. Soundness follows from backward induction. The theorem is classical, not a novelty claim.

The prophet value E[max_i X_i] is computed by the product of CDFs and independently checked by complete path enumeration. For any rational c, a witness with E[max_i X_i]-c*c_1>0 refutes the universal inequality E[max_i X_i]<=c*c_1 on any class containing that witness. Absence of a witness in a finite test collection proves nothing outside that collection.

## Nonnegativity caveat

Some prophet inequalities assume nonnegative random variables. Counterexamples with negative support do not refute those theorems. Users must independently verify that a generated witness satisfies every hypothesis of the target claim.
