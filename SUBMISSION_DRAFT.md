# Portal note (draft only; not submitted)

Research Novelty Bounty maintains a versioned novelty registry: each supported novel finding is accepted once and becomes context for the next judgment. The StudioNet demo shows F1 rewarded, its F2 paraphrase linked to F1 with no second reward, and distinct F3 rewarded against the updated registry. It also rejects a forged reveal and a duplicate reward claim. Commit/reveal is shared plumbing with Specification Bid Auction; the distinct mechanism is registry-dependent support and novelty judgment. Source bytes match the pushed commit; receipts separate FINALIZED from execution success. Rewards are synthetic units; this does not prove real custody or payment.

Character count: 665.

Evidence:

- [F1](https://explorer-studio.genlayer.com/tx/0x0c91adb9f51af4f2db4f5d4621f7246615b096826759c294998b902329e128d3) — FINALIZED / SUCCESS
- [F2](https://explorer-studio.genlayer.com/tx/0x1a979272838be096b076b16cafbf1f03b1c74f3ea567430bbcd5d8282e40fa1a) — FINALIZED / SUCCESS
- [F3](https://explorer-studio.genlayer.com/tx/0xf89b8f25772d8f30ad25832ed9c6274cd9435d6574b07bec838b42c6a782367e) — FINALIZED / SUCCESS
- [Expected failure: forged reveal](https://explorer-studio.genlayer.com/tx/0xe7e0b6ebfc52aa4d61da46d2bcbdf36b5730bbc7680492359dc38215d0b3f2a9) — FINALIZED / ERROR
- [Expected failure: duplicate reward](https://explorer-studio.genlayer.com/tx/0xd74d9d095efb127be0fc387ae8c31f73286da06db0d3aed8d617591065234bc9) — FINALIZED / ERROR

Rewards are synthetic units; the demo does not prove real custody or payment.

The repository is PRIVATE. Make it public manually before submitting. No Portal action was taken.
