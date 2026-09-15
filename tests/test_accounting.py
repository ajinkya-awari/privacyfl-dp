import pytest

from privacyfl_dp.accounting import AccountingRecord, validate_accounting_record


def test_missing_accountant_evidence_fails_closed_for_finite_measured_record():
    record = AccountingRecord(
        label="1.0",
        status="measured",
        target_epsilon=1.0,
        actual_epsilon=None,
        target_delta=1e-5,
        max_grad_norm=1.0,
        total_epochs=30,
        accountant_state=None,
        evidence_id="evidence-1",
        synthetic_only=False,
    )

    with pytest.raises(ValueError, match="actual_epsilon"):
        validate_accounting_record(record)


def test_actual_epsilon_above_target_fails_closed():
    record = AccountingRecord(
        label="0.5",
        status="measured",
        target_epsilon=0.5,
        actual_epsilon=0.51,
        target_delta=1e-5,
        max_grad_norm=1.0,
        total_epochs=30,
        accountant_state={"mechanism": "future-opacus"},
        evidence_id="evidence-2",
        synthetic_only=False,
    )

    with pytest.raises(ValueError, match="above target"):
        validate_accounting_record(record)


def test_missing_accountant_state_fails_closed():
    record = AccountingRecord(
        label="5.0",
        status="measured",
        target_epsilon=5.0,
        actual_epsilon=4.9,
        target_delta=1e-5,
        max_grad_norm=1.0,
        total_epochs=30,
        accountant_state=None,
        evidence_id="evidence-3",
        synthetic_only=False,
    )

    with pytest.raises(ValueError, match="accountant"):
        validate_accounting_record(record)


def test_synthetic_status_cannot_be_presented_as_measured_evidence():
    record = AccountingRecord(
        label="1.0",
        status="measured",
        target_epsilon=1.0,
        actual_epsilon=0.9,
        target_delta=1e-5,
        max_grad_norm=1.0,
        total_epochs=30,
        accountant_state={"mechanism": "synthetic-contract"},
        evidence_id="synthetic-evidence",
        synthetic_only=True,
    )

    with pytest.raises(ValueError, match="synthetic"):
        validate_accounting_record(record)


def test_no_dp_inf_record_uses_none_and_no_accountant_claim():
    record = AccountingRecord(
        label="inf",
        status="synthetic",
        target_epsilon=None,
        actual_epsilon=None,
        target_delta=None,
        max_grad_norm=None,
        total_epochs=30,
        accountant_state=None,
        evidence_id="synthetic-inf",
        synthetic_only=True,
    )

    validate_accounting_record(record)


def test_unknown_status_is_rejected():
    record = AccountingRecord(
        label="inf",
        status="complete",
        target_epsilon=None,
        actual_epsilon=None,
        target_delta=None,
        max_grad_norm=None,
        total_epochs=30,
        accountant_state=None,
        evidence_id="bad-status",
        synthetic_only=True,
    )

    with pytest.raises(ValueError, match="status"):
        validate_accounting_record(record)
