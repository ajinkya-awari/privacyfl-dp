from dataclasses import dataclass


EPSILON_LABELS = ("0.1", "0.5", "1.0", "5.0", "10.0", "inf")
NUM_CLIENTS = 5
FL_ROUNDS = 10
LOCAL_EPOCHS = 3
TOTAL_EPOCHS = FL_ROUNDS * LOCAL_EPOCHS
TARGET_DELTA = 1e-5
MAX_GRAD_NORM = 1.0


@dataclass(frozen=True)
class OperatingPoint:
    label: str
    target_epsilon: float | None
    target_delta: float | None
    max_grad_norm: float | None
    total_epochs: int
    privacy_engine_required: bool

    def to_record(self) -> dict[str, object]:
        return {
            "label": self.label,
            "target_epsilon": self.target_epsilon,
            "target_delta": self.target_delta,
            "max_grad_norm": self.max_grad_norm,
            "total_epochs": self.total_epochs,
            "privacy_engine_required": self.privacy_engine_required,
        }


def operating_point_for_label(label: str) -> OperatingPoint:
    if label not in EPSILON_LABELS:
        raise ValueError(f"unknown epsilon label: {label!r}")
    if label == "inf":
        return OperatingPoint(
            label=label,
            target_epsilon=None,
            target_delta=None,
            max_grad_norm=None,
            total_epochs=TOTAL_EPOCHS,
            privacy_engine_required=False,
        )
    target = float(label)
    if target <= 0:
        raise ValueError("finite epsilon labels must be positive")
    return OperatingPoint(
        label=label,
        target_epsilon=target,
        target_delta=TARGET_DELTA,
        max_grad_norm=MAX_GRAD_NORM,
        total_epochs=TOTAL_EPOCHS,
        privacy_engine_required=True,
    )


def build_operating_points() -> tuple[OperatingPoint, ...]:
    return tuple(operating_point_for_label(label) for label in EPSILON_LABELS)
