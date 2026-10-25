# Existing research software: comparison baseline (October 2026)

This is a preliminary, non-exhaustive landscape review. Feature absence is **not** established without hands-on evaluation. StopVerify does not claim a new Bellman algorithm or superiority to these tools.

| Project | Scope | Relationship to StopVerify | Source |
|---|---|---|---|
| PRISM | Probabilistic model checking for Markov decision processes, reward properties, and strategy synthesis | Strong verification baseline; assess whether StopVerify certificates add an easier independently checkable stopping-specific workflow | https://www.prismmodelchecker.org/ |
| Storm / stormpy | Probabilistic model checking, exact/sound analysis, expected rewards, Python interface | Closest challenge to a claim of exact verification novelty; compare precise rational guarantees and exported strategies | https://www.stormchecker.org/ |
| QuantEcon Dynamic Programming | Python/Julia models and code for optimal stopping and MDPs | Strong direct baseline for standard optimal-stopping computation and education | https://quantecon.github.io/book-dp1-public-companion/py/optimal_stopping.html |
| SDDP.jl | Multistage stochastic optimization via stochastic dual dynamic programming | More general and scalable; different emphasis from finite exact enumeration | https://sddp.dev/latest/ |
| pomdp-solve | Finite-horizon and discounted partially observable Markov decision processes | General dynamic-programming comparator; stopping is a special case | https://www.pomdp.org/code/ |
| R pomdp | R tooling for POMDP modeling and exact/approximate value iteration | Useful model/policy comparison; different language and target audience | https://cran.r-project.org/package=pomdp |
| msppy | Python multistage stochastic programming and SDDP | Adjacent stochastic optimization tool, not a direct certificate verifier comparison | https://github.com/lingquant/msppy |

## Questions to test experimentally

1. Can each tool encode the same finite independent stopping instance, including negative rewards and rational probabilities?
2. Does it produce an **exact rational** optimal value, and under which options?
3. Does it export a compact independently checkable witness/certificate of optimality?
4. Can a verifier reject a deliberately corrupted witness without rerunning the original solver?
5. Can it compute both the stopping value and the prophet benchmark from the same instance?
6. What is the cost (setup, runtime, memory) on a reproducible test suite?

## Working hypothesis (not a novelty claim)

A narrowly specified package for **exact, portable, independently checkable finite optimal-stopping certificates and prophet comparisons** may be useful to probability researchers. This hypothesis must be tested against PRISM, Storm and other tools before making publication claims.

## Initial audit examples

- Two observations: X1=1 and X2=0 or 2 with equal probability. Optimal stopping value 1; prophet value 3/2.
- Include rational ties, negative observations, deterministic observations and malformed JSON/certificates.
- Report exact fractions, not floating-point approximations.

## Publication decision gate

By December 2026, document at least one substantial external research use case, a feature-by-feature reproducible comparison with PRISM and Storm, and independent checker audit results. If no compelling differentiation emerges, reconsider scope or journal target.
