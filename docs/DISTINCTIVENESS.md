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

**Closest accepted match: Specification Bid Auction.** Both contracts use commit/reveal to bind a later disclosure to a prior commitment. That is shared plumbing. The distinct mechanism here is registry-dependent novelty judgment: a supported novel finding becomes part of the frozen context for the next serial judgment; an equivalent paraphrase links to an existing entry without reserving another reward. The registry version and snapshot/evidence digests bind the context validators compare.

**Evidence status (2026-10-12): PASS.** The direct suite passes 16 tests. Live F1 changed version 0 to 1; F2 used version 1 and linked to F-000001 with zero reward; F3 used version 1 and changed it to version 2. Forged reveal and duplicate reward failures were finalized and read back. See the current release manifest and command log. This is a local distinctiveness assessment; it does not prove ecosystem-wide originality or novelty across the internet.
