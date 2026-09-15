from dataclasses import dataclass
import re

from .accounting import EVIDENCE_STATUSES
from .config import EPSILON_LABELS


OVERCLAIM_PATTERN = re.compile(
    r"\b(clinical safety|formal privacy guarantee|hipaa compliant|secure aggregation is enabled|"
    r"proves privacy|proves clinical|deployment ready)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class MetricRecord:
    label: str
    status: str
    metric_name: str
    metric_value: float | None
    single_class_columns: tuple[str, ...]
    unsupported_reason: str | None


def validate_metric_record(record: MetricRecord) -> None:
    if record.label not in EPSILON_LABELS:
        raise ValueError("unknown metric label")
    if record.status not in EVIDENCE_STATUSES:
        raise ValueError("unknown metric status")
    if record.metric_name != "macro_auc":
        raise ValueError("only macro_auc schema is defined for this project")
    if record.status in {"planned", "synthetic"} and record.metric_value is not None:
        raise ValueError("synthetic or planned metric records must not contain metric values")
    if record.single_class_columns and not record.unsupported_reason:
        raise ValueError("single-class columns require an unsupported_reason")
    if record.metric_value is None and not (record.unsupported_reason or record.single_class_columns):
        raise ValueError("missing metric value requires an explicit unsupported reason")


def reject_overclaims(text: str) -> None:
    match = OVERCLAIM_PATTERN.search(text)
    if match:
        raise ValueError(f"unsupported claim rejected: {match.group(0)}")
