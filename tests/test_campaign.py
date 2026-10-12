import json

import pytest


SDK = "v0.6.0-rc5"
STANDARDS = [
    {"id": "traceable", "description": "The finding must be supported by retrievable primary evidence."},
    {"id": "scope", "description": "The finding must answer the frozen watershed research question."},
]
STANDARDS_JSON = json.dumps(STANDARDS)
REWARDS = [{"ordinal": 1, "reward_units": 30}, {"ordinal": 2, "reward_units": 20}, {"ordinal": 3, "reward_units": 10}]
REWARDS_JSON = json.dumps(REWARDS)
COMMIT_TIME = "2030-01-01T12:00:00Z"
COMMIT_DEADLINE = "2030-01-02T00:00:00Z"
REVEAL_TIME = "2030-01-03T12:00:00Z"
REVEAL_DEADLINE = "2030-01-05T00:00:00Z"
RESOLVE_TIME = "2030-01-06T00:00:01Z"
URL_A = "https://researcher-a.example.org/paper"
URL_B = "https://researcher-b.example.org/paper"
URL_C = "https://researcher-c.example.org/paper"


def llm(value) -> str:
    """The direct mock decodes once; the v0.6 SDK then parses JSON text."""
    return json.dumps(json.dumps(value))


def address_key(address):
    if isinstance(address, bytes):
        return "0x" + address.hex()
    return str(address).lower()


def deploy(direct_vm, direct_deploy, direct_owner, **overrides):
    args = {
        "campaign_id": "watershed-2030",
        "research_question": "Which measured land-use changes explain the recent nitrate increase in the North Basin?",
        "evidence_standards_json": STANDARDS_JSON,
        "reward_schedule_json": REWARDS_JSON,
        "budget_units": 100,
        "commit_deadline_iso": COMMIT_DEADLINE,
        "reveal_deadline_iso": REVEAL_DEADLINE,
    }
    args.update(overrides)
    direct_vm.sender = direct_owner
    direct_vm.warp(COMMIT_TIME)
    return direct_deploy(
        "contracts/research_novelty_bounty.py",
        args["campaign_id"],
        args["research_question"],
        args["evidence_standards_json"],
        args["reward_schedule_json"],
        args["budget_units"],
        args["commit_deadline_iso"],
        args["reveal_deadline_iso"],
        sdk_version=SDK,
    )


def commit(contract, direct_vm, researcher, claim, url, salt):
    refs = json.dumps([url])
    with direct_vm.prank(researcher):
        digest = contract.get_commitment_hash(claim, refs, salt)
        contract.commit_finding(digest)
    return researcher, claim, refs, salt


def reveal(contract, direct_vm, row):
    researcher, claim, refs, salt = row
    with direct_vm.prank(researcher):
        contract.reveal_finding(claim, refs, salt)


def test_original_finding_links_paraphrase_rewards_new_finding_and_conserves_budget(
    direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob, direct_charlie
):
    contract = deploy(direct_vm, direct_deploy, direct_owner)
    first = commit(
        contract, direct_vm, direct_alice,
        "North Basin nitrate rose after the 2028 upstream conversion increased winter runoff.",
        URL_A, "north-basin-original-salt-0001",
    )
    paraphrase = commit(
        contract, direct_vm, direct_bob,
        "The upstream land conversion in 2028 raised winter runoff and nitrate in North Basin.",
        URL_B, "north-basin-paraphrase-salt-02",
    )
    separate = commit(
        contract, direct_vm, direct_charlie,
        "A separate monitoring series shows the eastern tributary contributes the largest spring spike.",
        URL_C, "eastern-tributary-finding-salt-03",
    )

    direct_vm.warp(REVEAL_TIME)
    reveal(contract, direct_vm, first)
    reveal(contract, direct_vm, paraphrase)
    reveal(contract, direct_vm, separate)
    direct_vm.warp(RESOLVE_TIME)
    direct_vm.mock_web(r".*", {"status": 200, "body": "A public monitoring report with dated measurements and methods."})

    direct_vm.mock_llm(r"North Basin nitrate rose", llm({
        "support": "SUPPORTED", "novelty": "NOVEL", "nearest_entry_id": "", "citations": [URL_A],
    }))
    result = contract.resolve_next()
    assert result["status"] == "ACCEPTED_NOVEL"
    assert result["entry_id"] == "F-000001"
    assert result["reward_units"] == 30
    assert contract.get_registry()["version"] == 1
    assert direct_vm.run_validator()

    direct_vm.clear_mocks()
    direct_vm.mock_web(r".*", {"status": 200, "body": "A public monitoring report with dated measurements and methods."})
    direct_vm.mock_llm(r"raised winter runoff and nitrate in North Basin", llm({
        "support": "SUPPORTED", "novelty": "EQUIVALENT", "nearest_entry_id": "F-000001", "citations": [URL_B],
    }))
    result = contract.resolve_next()
    assert result["status"] == "LINKED_EQUIVALENT"
    assert contract.get_submission(address_key(direct_bob))["linked_entry_id"] == "F-000001"
    assert contract.get_registry()["version"] == 1
    assert contract.get_accounting()["reserved_units"] == 30
    assert direct_vm.run_validator()

    direct_vm.clear_mocks()
    direct_vm.mock_web(r".*", {"status": 200, "body": "A public monitoring report with dated measurements and methods."})
    direct_vm.mock_llm(r"separate monitoring series", llm({
        "support": "SUPPORTED", "novelty": "NOVEL", "nearest_entry_id": "", "citations": [URL_C],
    }))
    result = contract.resolve_next()
    assert result["status"] == "ACCEPTED_NOVEL"
    assert result["entry_id"] == "F-000002"
    assert result["reward_units"] == 20
    assert contract.get_submission(address_key(direct_charlie))["registry_version"] == 1
    assert contract.get_registry()["version"] == 2
    assert contract.get_campaign()["status"] == "CLOSED"
    assert direct_vm.run_validator()

    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("no accepted novelty reward is claimable"):
            contract.claim_reward()
        with direct_vm.expect_revert("only the campaign owner"):
            contract.refund_unspent_budget()
    with direct_vm.prank(direct_alice):
        assert contract.claim_reward() == 30
        with direct_vm.expect_revert("already been claimed"):
            contract.claim_reward()
    with direct_vm.prank(direct_charlie):
        assert contract.claim_reward() == 20
    with direct_vm.prank(direct_owner):
        assert contract.refund_unspent_budget() == 50
        with direct_vm.expect_revert("already been refunded"):
            contract.refund_unspent_budget()
    assert contract.get_accounting() == {
        "budget_units": 100,
        "available_units": 0,
        "reserved_units": 0,
        "paid_units": 50,
        "refunded_units": 50,
        "conserved": True,
    }


def test_changed_reveal_and_duplicate_commit_fail(direct_vm, direct_deploy, direct_owner, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_owner)
    row = commit(
        contract, direct_vm, direct_alice,
        "A report records a distinct long-term change in groundwater nitrate levels.",
        URL_A, "one-researcher-secret-salt-0001",
    )
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("only once"):
            contract.commit_finding("sha256:" + "a" * 64)
    direct_vm.warp(REVEAL_TIME)
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("does not match"):
            contract.reveal_finding("A different claim with changed content and meaning.", row[2], row[3])
    assert contract.get_submission(address_key(direct_alice))["status"] == "COMMITTED"
    reveal(contract, direct_vm, row)
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("already been revealed"):
            contract.reveal_finding(row[1], row[2], row[3])


@pytest.mark.parametrize("web_response", [
    pytest.param({"status": 503, "body": b"service unavailable"}, id="non-200"),
    pytest.param({"status": 200, "body": b""}, id="empty"),
    pytest.param({"status": 200, "body": b"x" * 5001}, id="oversized"),
    pytest.param({"status": 200, "body": b"\xff"}, id="invalid-utf8"),
])
def test_unavailable_sources_are_uncertain_and_refundable(direct_vm, direct_deploy, direct_owner, direct_alice, web_response):
    contract = deploy(direct_vm, direct_deploy, direct_owner)
    row = commit(
        contract, direct_vm, direct_alice,
        "The submitted finding has a distinct claim but its source is unavailable today.",
        URL_A, "unavailable-research-salt-0001",
    )
    direct_vm.warp(REVEAL_TIME)
    reveal(contract, direct_vm, row)
    direct_vm.warp(RESOLVE_TIME)
    direct_vm.mock_web(r".*", web_response)
    result = contract.resolve_next()
    assert result["status"] == "UNCERTAIN"
    source = contract.get_submission(address_key(direct_alice))["assessment"]["sources"][0]
    assert source["url"] == URL_A
    assert source["status"] == ("oversized" if len(web_response["body"]) > 5000 else "unavailable")
    assert source["byte_count"] == len(web_response["body"])
    assert contract.get_registry()["findings"] == []
    assert contract.get_accounting()["reserved_units"] == 0
    assert direct_vm.run_validator()
    with direct_vm.prank(direct_owner):
        assert contract.refund_unspent_budget() == 100
    assert contract.get_accounting()["conserved"] is True


def test_commit_reveal_and_resolution_deadline_boundaries(direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_owner)
    row = commit(
        contract, direct_vm, direct_alice,
        "This committed finding remains unrevealed and should not block later work.",
        URL_A, "unrevealed-priority-salt-0001",
    )
    direct_vm.warp(COMMIT_DEADLINE)
    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("commitment deadline has passed"):
            contract.commit_finding("sha256:" + "b" * 64)
    direct_vm.warp(REVEAL_DEADLINE)
    with direct_vm.expect_revert("reveal deadline has not passed"):
        contract.resolve_next()
    direct_vm.warp("2030-01-05T00:00:01Z")
    result = contract.resolve_next()
    assert result["status"] == "EXPIRED_UNREVEALED"
    assert contract.get_campaign()["status"] == "CLOSED"
    assert contract.get_submission(address_key(direct_alice))["status"] == "EXPIRED_UNREVEALED"


@pytest.mark.parametrize(
    "overrides, message",
    [
        ({"budget_units": 0}, "campaign budget must be a positive"),
        ({"reveal_deadline_iso": COMMIT_DEADLINE}, "reveal deadline must follow commit deadline"),
        ({"reward_schedule_json": json.dumps([{"ordinal": 2, "reward_units": 10}])}, "ordinals must be contiguous"),
        ({"reward_schedule_json": json.dumps(REWARDS + [{"ordinal": 4, "reward_units": 100}])}, "exceeds campaign budget"),
    ],
)
def test_constructor_freezes_and_validates_campaign_terms(direct_vm, direct_deploy, direct_owner, overrides, message):
    with direct_vm.expect_revert(message):
        deploy(direct_vm, direct_deploy, direct_owner, **overrides)


def test_invalid_evidence_host_rejected_before_commit(direct_vm, direct_deploy, direct_owner, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_owner)
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("public DNS hostname"):
            contract.get_commitment_hash(
                "This finding claims a measured change in nitrate concentration.",
                json.dumps(["https://127.0.0.1/private"]),
                "long-enough-private-salt-0001",
            )
