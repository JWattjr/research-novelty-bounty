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

The current direct-mode run passed 15 tests. GenVM lint passed 3 checks, contract validation identified 12 methods (6 views, 6 writes), and schema extraction succeeded. The live StudioNet attempt is recorded separately: deployment and the first resolution finalized, but support was UNCERTAIN and the demonstration stopped without retry.
