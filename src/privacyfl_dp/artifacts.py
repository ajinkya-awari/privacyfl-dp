from dataclasses import dataclass
import re
from pathlib import PurePosixPath
from typing import Mapping


ARTIFACT_STATUSES = ("planned", "not-created", "synthetic", "measured", "reviewed", "released")
REQUIRED_PROVENANCE_FIELDS = (
    "source_profile_id",
    "partition_id",
    "config_revision",
    "seed",
    "created_by",
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_PARTS = {"data", "raw", "models", "model", "checkpoints", "checkpoint", "weights"}
FORBIDDEN_SUFFIXES = {".pt", ".pth", ".ckpt", ".onnx", ".bin", ".safetensors", ".csv"}


@dataclass(frozen=True)
class ArtifactManifest:
    artifact_id: str
    path: str
    status: str
    sha256: str | None
    provenance: Mapping[str, object]


def validate_artifact_manifest(manifest: ArtifactManifest) -> None:
    if not manifest.artifact_id:
        raise ValueError("artifact_id is required")
    if manifest.status not in ARTIFACT_STATUSES:
        raise ValueError("invalid artifact status")
    _validate_safe_path(manifest.path)
    if manifest.sha256 is not None and not SHA256_PATTERN.fullmatch(manifest.sha256):
        raise ValueError("sha256 must be 64 lowercase hexadecimal characters")
    missing = [field for field in REQUIRED_PROVENANCE_FIELDS if field not in manifest.provenance]
    if missing:
        raise ValueError(f"provenance missing fields: {missing}")


def _validate_safe_path(path: str) -> None:
    normalized = path.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError("path traversal or absolute path is not allowed")
    lowered_parts = {part.lower() for part in pure.parts}
    if lowered_parts.intersection(FORBIDDEN_PARTS) or pure.suffix.lower() in FORBIDDEN_SUFFIXES:
        raise ValueError("artifact path must not point to raw data, model, weight, or checkpoint files")
