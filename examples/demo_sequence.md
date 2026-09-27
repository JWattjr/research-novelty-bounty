# Reproducible demo sequence

Run the full direct-mode example:

```powershell
python -m pytest tests/test_campaign.py::test_original_finding_links_paraphrase_rewards_new_finding_and_conserves_budget
```

It uses [constructor.json](constructor.json) and three researcher accounts:

1. Alice commits a finding that winter runoff increased after a specific 2028 upstream conversion. Bob commits a paraphrase. Charlie commits a separate eastern-tributary finding. Each commitment includes sender, campaign, contract, claim, reference URL, and salt.
2. All three reveal within the window. Their queue order is the transaction order of the commitments.
3. Alice resolves first against registry version 0. The mocked independent assessment marks the finding supported and novel. The contract appends `F-000001`, advances to version 1, and reserves 30 demo units.
4. Bob resolves against version 1. His paraphrase links to `F-000001`; the registry and reward reservation do not change.
5. Charlie resolves against version 1. His supported distinct finding becomes `F-000002`, advances the registry to version 2, and reserves the ordinal-two reward of 20.
6. Alice and Charlie claim 30 and 20 once. The campaign owner refunds the remaining 50 of the 100-unit demo budget. The final accounting conserves the original budget.

The test mocks web/model I/O. It demonstrates local state and validator behavior, not live network consensus or scientific proof.
