import json

from privacyfl_dp.synthetic_verify import build_synthetic_evidence


def test_synthetic_verification_record_is_sanitized_and_contract_only():
    record = build_synthetic_evidence(seed=17)
    payload = json.dumps(record, sort_keys=True)

    assert record["status"] == "synthetic"
    assert record["scope"] == "local synthetic contract only"
    assert record["client_count"] == 5
    assert record["total_epochs"] == 30
    assert record["measured_epsilon"] is None
    assert record["measured_auc"] is None
    assert "patient" not in payload.lower()
    assert "chestx" not in payload.lower()
