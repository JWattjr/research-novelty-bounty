# Security notes

## Authority and judgment

- The campaign owner freezes the question, standards, schedule, budget, and deadlines at construction. There is no update path.
- A researcher is identified by sender address and may make one commitment. Salts should be random and secret until reveal. The hash also binds the contract and campaign, preventing cross-campaign replay.
- Submission order is the deterministic order of commitment transactions. The contract does not claim this is proof of who discovered information first in the real world.
- The leader assesses one finding against one exact snapshot. Validators independently fetch and assess the same claim and registry; the validator rejects malformed fields, an incorrect snapshot digest, unsubmitted citations, an invalid equivalent link, or a different substantive status vector.
- The model does not choose reward values or mutate balances. Ordinal rewards, registry entry IDs, queue movement, reward claims, and refunds are deterministic.

## Evidence and failure behavior

- The fetcher accepts only HTTP 200 responses with nonempty UTF-8 bodies up to 5,000 bytes. URLs are syntax-checked for HTTPS and public-DNS hostnames, but DNS resolution, redirects, publisher identity, signatures, and timestamps are not verified.
- Retrieved text and submitted claims are untrusted data. The prompt requests campaign-local comparison and asks the model to ignore embedded instructions. This does not remove prompt injection or model error risk.
- If all submitted references are unavailable, the only valid assessment is `UNCERTAIN`. Unsupported or uncertain findings receive no reward. If consensus or parsing fails, the transaction reverts and the resolution cursor does not advance.
- A supported `NOVEL` judgment is only novel against the registry version in its digest. The next queue item uses the updated version. If the configured reward schedule is exhausted, the remaining item is closed as `REJECTED_REWARD_CAP` without creating an unfunded entry.

## Accounting and scope

- Constructor budget is synthetic demo units; there is no token/native-value custody. New entries reserve exactly one fixed schedule amount. Claiming moves that amount from reserved to paid; the owner may refund only unreserved budget after close, once.
- At most eight submissions, eight registry entries, eight evidence standards, and three references per finding are processed. Submission history is bounded by the queue cap.
- Direct tests use mocked I/O. They do not verify live validator behavior, source freshness, network finality, or deployment compatibility. This contract is undeployed and has no Portal receipt.
