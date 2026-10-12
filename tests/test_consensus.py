import hashlib
import json

from test_campaign import URL_A, URL_B, address_key, commit, deploy, llm, reveal


def test_validator_rejects_disagreement_stale_versions_and_forged_leader_fields(
    direct_vm, direct_deploy, direct_owner, direct_alice
):
    contract = deploy(direct_vm, direct_deploy, direct_owner)
    row = commit(
        contract, direct_vm, direct_alice,
        "A dated survey documents a separate shift in nitrate concentration.",
        URL_A, "validator-finding-salt-0001",
    )
    direct_vm.warp("2030-01-03T12:00:00Z")
    reveal(contract, direct_vm, row)
    direct_vm.warp("2030-01-06T00:00:01Z")
    direct_vm.mock_web(r".*", {"status": 200, "body": "Survey with dated measurements and methods."})
    direct_vm.mock_llm(r"separate shift in nitrate", llm({
        "support": "SUPPORTED", "novelty": "NOVEL", "nearest_entry_id": "", "citations": [URL_A],
    }))
    contract.resolve_next()
    assert direct_vm.run_validator()
    record = contract.get_submission(address_key(direct_alice))
    honest = {
        "input_snapshot_digest": record["input_snapshot_digest"],
        "snapshot_digest": record["snapshot_digest"],
        "evidence_digest": record["evidence_digest"],
        "assessment": record["assessment"],
    }

    disagreement = json.loads(json.dumps(honest))
    disagreement["assessment"]["support"] = "UNSUPPORTED"
    assert direct_vm.run_validator(leader_result=disagreement) is False

    stale = json.loads(json.dumps(honest))
    stale["snapshot_digest"] = "sha256:" + "0" * 64
    assert direct_vm.run_validator(leader_result=stale) is False

    extra = json.loads(json.dumps(honest))
    extra["assessment"]["model_reasoning"] = "leader metadata must not enter the accepted schema"
    assert direct_vm.run_validator(leader_result=extra) is False

    invented_link = json.loads(json.dumps(honest))
    invented_link["assessment"]["novelty"] = "EQUIVALENT"
    invented_link["assessment"]["nearest_entry_id"] = "F-999999"
    assert direct_vm.run_validator(leader_result=invented_link) is False


def test_validator_rejects_forged_citation_with_same_novelty_and_support(
    direct_vm, direct_deploy, direct_owner, direct_alice
):
    contract = deploy(direct_vm, direct_deploy, direct_owner)
    claim = "A dated survey documents a separate shift in nitrate concentration."
    refs = json.dumps([URL_A, URL_B])
    salt = "same-headline-citation-salt-01"
    with direct_vm.prank(direct_alice):
        digest = contract.get_commitment_hash(claim, refs, salt)
        contract.commit_finding(digest)
    direct_vm.warp("2030-01-03T12:00:00Z")
    with direct_vm.prank(direct_alice):
        contract.reveal_finding(claim, refs, salt)
    direct_vm.warp("2030-01-06T00:00:01Z")
    direct_vm.mock_web(r".*", {"status": 200, "body": "Survey with dated measurements and methods."})
    direct_vm.mock_llm(r"separate shift in nitrate", llm({
        "support": "SUPPORTED", "novelty": "NOVEL", "nearest_entry_id": "", "citations": [URL_A],
    }))
    contract.resolve_next()
    record = contract.get_submission(address_key(direct_alice))
    honest = {
        "input_snapshot_digest": record["input_snapshot_digest"],
        "snapshot_digest": record["snapshot_digest"],
        "evidence_digest": record["evidence_digest"],
        "assessment": record["assessment"],
    }
    forged = json.loads(json.dumps(honest))
    forged["assessment"]["citations"] = [URL_B]
    assert forged["assessment"]["support"] == honest["assessment"]["support"]
    assert forged["assessment"]["novelty"] == honest["assessment"]["novelty"]
    assert direct_vm.run_validator(leader_result=forged) is False
    forged_evidence = json.loads(json.dumps(honest))
    forged_evidence["evidence_digest"] = "sha256:" + "0" * 64
    digest_input = {
        "input_snapshot_digest": forged_evidence["input_snapshot_digest"],
        "evidence_digest": forged_evidence["evidence_digest"],
    }
    canonical = json.dumps(digest_input, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    forged_evidence["snapshot_digest"] = "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert direct_vm.run_validator(leader_result=forged_evidence) is False

def test_source_availability_is_stored_and_validator_compared(
    direct_vm, direct_deploy, direct_owner, direct_alice
):
    contract = deploy(direct_vm, direct_deploy, direct_owner)
    row = commit(contract, direct_vm, direct_alice,
        "A dated survey documents a separate shift in nitrate concentration.",
        URL_A, "availability-finding-salt-0001")
    direct_vm.warp("2030-01-03T12:00:00Z")
    reveal(contract, direct_vm, row)
    direct_vm.warp("2030-01-06T00:00:01Z")
    body = "Survey with dated measurements and methods."
    direct_vm.mock_web(r".*", {"status": 200, "body": body})
    direct_vm.mock_llm(r"separate shift in nitrate", llm({
        "support": "SUPPORTED", "novelty": "NOVEL", "nearest_entry_id": "", "citations": [URL_A],
    }))
    contract.resolve_next()
    record = contract.get_submission(address_key(direct_alice))
    assert record["assessment"]["sources"] == [{"url": URL_A, "status": "fetched", "byte_count": len(body.encode())}]
    assert direct_vm.run_validator()
    honest = {key: record[key] for key in ("input_snapshot_digest", "snapshot_digest", "evidence_digest", "assessment")}
    forged = json.loads(json.dumps(honest))
    forged["assessment"]["sources"][0]["byte_count"] += 1
    assert direct_vm.run_validator(leader_result=forged) is False
    forged = json.loads(json.dumps(honest))
    forged["assessment"]["sources"][0]["status"] = "unavailable"
    assert direct_vm.run_validator(leader_result=forged) is False
