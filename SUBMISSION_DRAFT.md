# Submission draft — not deployed or submitted

**Status: local draft only. This contract is undeployed and has not been submitted to the GenLayer Portal.**

## Project

`ResearchNoveltyBounty` accepts one secret-then-revealed finding per researcher and processes submissions in commitment order. GenLayer independently evaluates support and campaign-local novelty against a registry version bound into the judgment snapshot. A supported novel finding extends the registry and reserves one predetermined ordinal reward; an equivalent finding links to an existing entry without a second reward.

## Differentiating mechanism

The registry mutates as accepted findings arrive. The next submission is judged against the new version, so an earlier novelty comparison cannot authorize a duplicate reward. The commitment sequence defines campaign processing priority; it is not a claim to real-world discovery priority.

## Local verification recorded

- GenVM lint: passed 3 checks.
- Contract validation: 12 methods (6 views, 6 writes).
- ABI schema extraction: succeeded to `contracts/abi.json`.
- Direct-mode tests: 10 passed, including supported novelty, equivalent linking, stale snapshots, forged leader data, unavailable evidence, and conservation.
- Live deployment, finality receipts, real rewards, and Portal review: not performed.

## Limitations

Novelty is limited to the bounded campaign registry. Demo units are not backed by real assets. Direct tests mock evidence and model calls and do not prove live consensus, publisher identity, global originality, or scientific truth. This draft makes no originality or Portal-score guarantee.
