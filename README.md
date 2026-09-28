# Research Novelty Bounty

`ResearchNoveltyBounty` rewards supported findings that are materially new within one bounded campaign registry. Researchers commit identity-bound hashes before a reveal window. The contract resolves revealed submissions in commit order. Each judgment includes the exact registry version and snapshot digest, so later work cannot reuse a comparison against an earlier registry state. A supported novel finding appends one entry and reserves the reward at that ordinal. An equivalent finding links to an existing entry without another reward.

Campaign-local novelty is the only novelty claim. This contract does not search or prove uniqueness across the internet.

## Toolchain

The source pins py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6. The installed GenVM linter validates this header. A StudioNet deployment from the recorded source commit finalized successfully, and the deployed source matched its Git blob. The local v0.6 RC development dependencies are pinned in requirements.txt.

Install Python 3.14 and run:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
genvm-lint lint contracts/research_novelty_bounty.py
genvm-lint validate contracts/research_novelty_bounty.py
genvm-lint schema contracts/research_novelty_bounty.py --output contracts/abi.json
python -m pytest
```

Direct-mode tests use mocked web and model responses. They execute the contract and validator closure locally but do not demonstrate live network consensus, deployment finality, or live source availability.

## Lifecycle

1. The campaign owner freezes the research question, 1–8 evidence standards, ordinal reward schedule, demo budget, and commit/reveal deadlines. The schedule total cannot exceed the budget.
2. A researcher commits one `sha256:` digest. It binds the contract address, campaign ID, researcher address, claim, evidence URLs, and salt. Only the digest is visible before reveal.
3. During the reveal window, the researcher reveals the exact claim, references, and salt. The queue preserves commitment transaction order. Unrevealed queue entries expire without blocking later entries.
4. After the reveal deadline, anyone may call `resolve_next`. Each revealed entry is evaluated against the current bounded registry. The independent validator rechecks support and novelty and must agree on the substantive status vector. The snapshot digest binds the registry version and exact submission.
5. Unsupported or uncertain claims do not enter the registry. An equivalent claim links to its exact existing entry and receives no reward. A supported novel claim creates the next deterministic `F-000001`-style entry and reserves that ordinal's fixed reward.
6. The researcher can claim a reserved reward once. Once all queued submissions have been handled, the campaign closes; the owner may refund unreserved budget once. Any outstanding reward reservation remains protected after close.

## API

Constructor inputs are in [examples/constructor.json](examples/constructor.json). Main writes are `commit_finding`, `reveal_finding`, `resolve_next`, `close_empty_campaign`, `claim_reward`, and `refund_unspent_budget`. Views are `get_commitment_hash`, `get_campaign`, `get_registry`, `get_submission`, `get_history`, and `get_accounting`. See [contracts/abi.json](contracts/abi.json) for the generated ABI.

## Limits

The prototype allows at most eight commitments, eight standards, eight rewarded registry entries, and three evidence URLs per submission. Evidence URLs must use HTTPS and a public-DNS hostname; bodies must be nonempty UTF-8 and no more than 5,000 bytes. The contract does not authenticate publishers, verify signatures, resolve DNS, or validate document freshness. Fetched text is untrusted prompt input. No available source yields `UNCERTAIN`; malformed consensus output reverts resolution without advancing the queue.

Rewards are synthetic demo units and do not represent a token, native value, or real payment. The first live support judgment finalized as UNCERTAIN; the campaign stopped with one revealed submission unresolved, no registry entry, and no reward. No Portal submission occurred.

See [mechanism differentiation](docs/MECHANISM_DIFFERENTIATION.md), [test matrix](docs/TEST_MATRIX.md), [security notes](docs/SECURITY_NOTES.md), [demo sequence](examples/demo_sequence.md), and the [submission draft](SUBMISSION_DRAFT.md).
