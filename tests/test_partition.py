import pytest

from privacyfl_dp.partition import (
    SyntheticPartition,
    build_synthetic_partition,
    validate_partition,
)


def test_synthetic_partition_has_five_deterministic_non_overlapping_clients():
    first = build_synthetic_partition(records_per_client=4, evaluation_records=3, seed=17)
    second = build_synthetic_partition(records_per_client=4, evaluation_records=3, seed=17)

    assert first == second
    assert len(first.client_shards) == 5
    assert tuple(sorted(first.client_shards)) == (0, 1, 2, 3, 4)
    validate_partition(first)


def test_client_partition_overlap_fails_closed():
    partition = SyntheticPartition(
        seed=1,
        client_shards={
            0: ("synthetic_a", "synthetic_b"),
            1: ("synthetic_b",),
            2: ("synthetic_c",),
            3: ("synthetic_d",),
            4: ("synthetic_e",),
        },
        evaluation_ids=("synthetic_eval",),
    )

    with pytest.raises(ValueError, match="overlap"):
        validate_partition(partition)


def test_evaluation_records_cannot_appear_in_training_shards():
    partition = SyntheticPartition(
        seed=1,
        client_shards={
            0: ("synthetic_eval",),
            1: ("synthetic_train_1",),
            2: ("synthetic_train_2",),
            3: ("synthetic_train_3",),
            4: ("synthetic_train_4",),
        },
        evaluation_ids=("synthetic_eval",),
    )

    with pytest.raises(ValueError, match="evaluation"):
        validate_partition(partition)


def test_client_count_is_exactly_five():
    partition = SyntheticPartition(
        seed=1,
        client_shards={0: ("a",), 1: ("b",), 2: ("c",), 3: ("d",)},
        evaluation_ids=("e",),
    )

    with pytest.raises(ValueError, match="five"):
        validate_partition(partition)
