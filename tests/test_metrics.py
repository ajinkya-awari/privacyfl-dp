import pytest

from privacyfl_dp.metrics import MetricRecord, reject_overclaims, validate_metric_record


def test_synthetic_metric_schema_requires_single_class_handling():
    record = MetricRecord(
        label="1.0",
        status="synthetic",
        metric_name="macro_auc",
        metric_value=None,
        single_class_columns=("Finding A",),
        unsupported_reason="single-class column skipped in synthetic schema check",
    )

    validate_metric_record(record)


def test_metric_value_for_synthetic_status_is_rejected():
    record = MetricRecord(
        label="1.0",
        status="synthetic",
        metric_name="macro_auc",
        metric_value=0.91,
        single_class_columns=(),
        unsupported_reason=None,
    )

    with pytest.raises(ValueError, match="synthetic"):
        validate_metric_record(record)


def test_clinical_and_privacy_overclaims_are_rejected():
    claims = (
        "This proves clinical safety.",
        "The synthetic record gives a formal privacy guarantee.",
        "The model is HIPAA compliant.",
        "Secure aggregation is enabled.",
    )

    for claim in claims:
        with pytest.raises(ValueError):
            reject_overclaims(claim)
