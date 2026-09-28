# Distinctiveness audit

Scope: contract source review against the other nine portfolio contracts, the named standalone contracts, and the closest local projects. This is a local comparison, not an ecosystem-wide originality claim.

**Disposition: KEEP.** The mechanism is the campaign-local, versioned support-and-novelty registry with serial reward allocation; it does not claim novelty across the internet.

| Closest comparator | Its judgment | Participants and actions | Its state changes | Capability or invariant implemented here |
|---|---|---|---|---|
| Standalone ClaimNet Semantic Exposure Graph | Classifies the relation and risk band between two immutable market claims. | An owner supplies exactly two claims and invokes classification. | Stores one pairwise result and attempt count. | Each revealed finding is assessed for evidence support and equivalence to a versioned campaign registry; a supported equivalent links to one prior entry and earns no second reward. |
| Standalone Token Claim Capability Gate | Classifies a frozen list of token claims against context and public sources. | A deployer fixes one token manifest and a public review finalizes it. | Derives one terminal gate from per-claim states. | A bounded sequence of independently revealed researchers changes the registry between judgments, so each snapshot binds the exact earlier entries and reward slot. |
| Standalone QuestChain | Judges milestone statuses, then derives masks, streaks, and points. | A quest owner configures milestones; callers resolve and claim rewards. | Advances one quest's progress and point accounting. | Reward order is tied to serial submissions, while novelty links and accepted entries persist as campaign state for later researchers. |
| New Specification Bid Auction | Classifies supplier bids against requirements, then picks the lowest eligible price. | Buyer freezes a job; suppliers commit and reveal. | Creates one winner and an acceptance/refund lifecycle. | This contract tests evidence-backed research findings and campaign-local equivalence; it does not rank suppliers by price. |
| Standalone TruthGraph | Resolves a fixed graph of predicates against fetched evidence. | An owner supplies the graph and sources; callers trigger resolution. | Stores an outcome and retries for one market. | A finding can extend the registry, affect the next queued submission's frozen context, and receive one scheduled reward. |

The distinction is local: the older comparators store a fixed review or pairwise classification, while this contract evolves a campaign registry and reward queue. The source is in contracts/research_novelty_bounty.py (_snapshot, _consensus_assessment, resolve_next, claim_reward).

**Evidence status:** implemented; the current direct suite passes 15 tests, and the documented Phase 3 cases are covered. This contract deployed from the recorded source commit and its deployed blob matched Git. The live original-finding judgment finalized as support=UNCERTAIN and novelty=NOVEL after four rounds; the second finding remains revealed and unresolved. The run stopped without retry, reward, or public release. This is a local distinction claim, not ecosystem-wide originality.
