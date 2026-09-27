import json

from test_campaign import URL_A, address_key, commit, deploy, llm, reveal


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
        "snapshot_digest": record["snapshot_digest"],
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
