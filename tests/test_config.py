import pytest

from privacyfl_dp.config import (
    EPSILON_LABELS,
    FL_ROUNDS,
    LOCAL_EPOCHS,
    MAX_GRAD_NORM,
    NUM_CLIENTS,
    TARGET_DELTA,
    TOTAL_EPOCHS,
    build_operating_points,
    operating_point_for_label,
)


def test_operating_points_match_project_contract():
    assert EPSILON_LABELS == ("0.1", "0.5", "1.0", "5.0", "10.0", "inf")
    assert NUM_CLIENTS == 5
    assert FL_ROUNDS == 10
    assert LOCAL_EPOCHS == 3
    assert TOTAL_EPOCHS == 30
    assert TOTAL_EPOCHS == FL_ROUNDS * LOCAL_EPOCHS
    assert TARGET_DELTA == 1e-5
    assert MAX_GRAD_NORM == 1.0

    points = build_operating_points()
    assert tuple(point.label for point in points) == EPSILON_LABELS


def test_inf_serializes_to_none_without_numeric_epsilon():
    point = operating_point_for_label("inf")

    assert point.target_epsilon is None
    assert point.target_delta is None
    assert point.max_grad_norm is None
    assert point.privacy_engine_required is False
    assert point.to_record()["target_epsilon"] is None


def test_finite_epsilon_labels_are_numeric_positive_and_fixed_controls():
    for label in EPSILON_LABELS:
        if label == "inf":
            continue
        point = operating_point_for_label(label)
        assert point.target_epsilon == float(label)
        assert point.target_epsilon > 0
        assert point.target_delta == 1e-5
        assert point.max_grad_norm == 1.0
        assert point.total_epochs == 30
        assert point.privacy_engine_required is True


def test_invalid_epsilon_labels_are_rejected():
    for label in ("", "0", "-1.0", "infinity", "nan", "2.0"):
        with pytest.raises(ValueError):
            operating_point_for_label(label)
