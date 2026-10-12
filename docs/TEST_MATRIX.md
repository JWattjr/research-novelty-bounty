# Test matrix

Run `python -m pytest` from the repository root. Tests use mocked direct-mode responses and do not establish live network consensus.

| Invariant or behavior | Test |
|---|---|
| Original supported finding earns ordinal one; equivalent paraphrase links without reward; a separate finding is judged against registry version one and earns ordinal two; reward claims and refund conserve budget | `test_original_finding_links_paraphrase_rewards_new_finding_and_conserves_budget` |
| One commit per sender, changed reveal rejection, and one-time reveal | `test_changed_reveal_and_duplicate_commit_fail` |
| Unavailable source remains uncertain and earns no reward; budget can be refunded after close | `test_unavailable_sources_are_uncertain_and_refundable` |
| Exact commitment and reveal deadline boundaries; unrevealed priority slot expires | `test_commit_reveal_and_resolution_deadline_boundaries` |
| Budget, deadline order, ordinal schedule, and schedule/budget bound are frozen and validated | `test_constructor_freezes_and_validates_campaign_terms` (four parameter cases) |
| Local and IP-literal evidence references are rejected | `test_invalid_evidence_host_rejected_before_commit` |
| Validator rejects altered support, stale snapshot digest, extra leader metadata, and a nonexistent equivalent entry | `test_validator_rejects_disagreement_stale_versions_and_forged_leader_fields` |

| Every model-returned judgment field is validated and compared or bound to frozen input | `test_every_returned_judgment_field_is_compared_or_snapshot_bound` |
| HTTP error, empty body, oversized body, invalid UTF-8 all yield uncertainty and no reward | `test_unavailable_sources_are_uncertain_and_refundable` (four response cases) |
| Validator rejects a changed submitted citation and forged evidence digest with support and novelty unchanged | `test_validator_rejects_forged_citation_with_same_novelty_and_support` |

| Per-source fetched status and byte count survive storage; validator rejects forged availability and byte count | `test_source_availability_is_stored_and_validator_compared` |

The 2026-10-12 direct-mode suite passed **16 tests**. GenVM `check` passed three AST checks and SDK validation (12 methods). The pinned runner is unchanged. These tests are mocked local execution and do not contact the localnet URL printed by gltest configuration.

The historical 2026-09-28 run had uncertain support. The complete source digest matches; Client/AsyncClient did not occur in the source text. The new live attempt is recorded in `deployments/studionet-release-2026-10-12.json`.

| Live behavior | Recorded result |
|---|---|
| `deploy_campaign` | FINALIZED / leader SUCCESS; [Explorer](https://explorer-studio.genlayer.com/tx/0x8edcf5cddd6400466ffc81b07d5dcfb5479a24c1c3a71c52cd59eb3b9a0e69c1) |
| `resolve_next:F1` | FINALIZED / leader SUCCESS; [Explorer](https://explorer-studio.genlayer.com/tx/0x0c91adb9f51af4f2db4f5d4621f7246615b096826759c294998b902329e128d3) |
| `resolve_next:F2` | FINALIZED / leader SUCCESS; [Explorer](https://explorer-studio.genlayer.com/tx/0x1a979272838be096b076b16cafbf1f03b1c74f3ea567430bbcd5d8282e40fa1a) |
| `resolve_next:F3` | FINALIZED / leader SUCCESS; [Explorer](https://explorer-studio.genlayer.com/tx/0xf89b8f25772d8f30ad25832ed9c6274cd9435d6574b07bec838b42c6a782367e) |
| `reveal_finding:forged_F3` | FINALIZED / leader ERROR; [Explorer](https://explorer-studio.genlayer.com/tx/0xe7e0b6ebfc52aa4d61da46d2bcbdf36b5730bbc7680492359dc38215d0b3f2a9) |
| `claim_reward:duplicate_F1` | FINALIZED / leader ERROR; [Explorer](https://explorer-studio.genlayer.com/tx/0xd74d9d095efb127be0fc387ae8c31f73286da06db0d3aed8d617591065234bc9) |

Each completed commit, reveal, resolution and claim has a recorded read-back. Expected failures require the exact rejection reason and preserved state; lifecycle acceptance alone does not prove success.
