from dataclasses import dataclass
from typing import Mapping

from .config import EPSILON_LABELS, MAX_GRAD_NORM, TARGET_DELTA, TOTAL_EPOCHS


EVIDENCE_STATUSES = ("planned", "synthetic", "measured", "reviewed", "released")
MEASURED_STATUSES = {"measured", "reviewed", "released"}


@dataclass(frozen=True)
class AccountingRecord:
    label: str
    status: str
    target_epsilon: float | None
    actual_epsilon: float | None
    target_delta: float | None
    max_grad_norm: float | None
    total_epochs: int
    accountant_state: Mapping[str, object] | None
    evidence_id: str
    synthetic_only: bool


def validate_accounting_record(record: AccountingRecord) -> None:
    if record.status not in EVIDENCE_STATUSES:
        raise ValueError(f"status must be one of {EVIDENCE_STATUSES}")
    if record.label not in EPSILON_LABELS:
        raise ValueError("unknown accounting label")
    if record.total_epochs != TOTAL_EPOCHS:
        raise ValueError("total_epochs must equal FL_ROUNDS * LOCAL_EPOCHS")
    if not record.evidence_id:
        raise ValueError("evidence_id is required")
    if record.synthetic_only and record.status in MEASURED_STATUSES:
        raise ValueError("synthetic evidence cannot be presented as measured evidence")

    if record.label == "inf":
        if record.target_epsilon is not None or record.actual_epsilon is not None:
            raise ValueError("inf records must use target_epsilon=None and actual_epsilon=None")
        if record.target_delta is not None or record.max_grad_norm is not None:
            raise ValueError("inf records must not claim DP delta or clipping")
        return

    target = float(record.label)
    if record.target_epsilon != target:
        raise ValueError("finite record target_epsilon does not match label")
    if record.target_delta != TARGET_DELTA:
        raise ValueError("finite record target_delta must be 1e-5")
    if record.max_grad_norm != MAX_GRAD_NORM:
        raise ValueError("finite record max_grad_norm must be 1.0")

    if record.status in MEASURED_STATUSES:
        if record.actual_epsilon is None:
            raise ValueError("finite measured record requires actual_epsilon")
        if record.accountant_state is None:
            raise ValueError("finite measured record requires accountant state")
        if record.actual_epsilon > target:
            raise ValueError("actual_epsilon above target")
