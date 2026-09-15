from dataclasses import dataclass
import random

from .config import NUM_CLIENTS


@dataclass(frozen=True)
class SyntheticPartition:
    seed: int
    client_shards: dict[int, tuple[str, ...]]
    evaluation_ids: tuple[str, ...]


def build_synthetic_partition(
    records_per_client: int,
    evaluation_records: int,
    seed: int,
) -> SyntheticPartition:
    if records_per_client <= 0:
        raise ValueError("records_per_client must be positive")
    if evaluation_records <= 0:
        raise ValueError("evaluation_records must be positive")
    rng = random.Random(seed)
    client_shards: dict[int, tuple[str, ...]] = {}
    for client_id in range(NUM_CLIENTS):
        client_shards[client_id] = tuple(
            f"synthetic_train_c{client_id}_{index}_{rng.randrange(10**9):09d}"
            for index in range(records_per_client)
        )
    evaluation_ids = tuple(
        f"synthetic_eval_{index}_{rng.randrange(10**9):09d}"
        for index in range(evaluation_records)
    )
    partition = SyntheticPartition(
        seed=seed,
        client_shards=client_shards,
        evaluation_ids=evaluation_ids,
    )
    validate_partition(partition)
    return partition


def validate_partition(partition: SyntheticPartition) -> None:
    if len(partition.client_shards) != NUM_CLIENTS:
        raise ValueError("synthetic partition must contain exactly five clients")
    if set(partition.client_shards) != set(range(NUM_CLIENTS)):
        raise ValueError("synthetic partition client IDs must be 0 through 4")

    seen_training: set[str] = set()
    for client_id, record_ids in partition.client_shards.items():
        if not record_ids:
            raise ValueError(f"client {client_id} has no records")
        overlap = seen_training.intersection(record_ids)
        if overlap:
            raise ValueError(f"client partition overlap detected: {sorted(overlap)}")
        seen_training.update(record_ids)

    evaluation = set(partition.evaluation_ids)
    if not evaluation:
        raise ValueError("evaluation records are required")
    leakage = seen_training.intersection(evaluation)
    if leakage:
        raise ValueError(f"evaluation leakage detected: {sorted(leakage)}")
