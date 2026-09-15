from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .artifacts import ArtifactManifest, validate_artifact_manifest
from .config import TOTAL_EPOCHS, build_operating_points
from .partition import build_synthetic_partition


def build_synthetic_evidence(seed: int = 17) -> dict[str, Any]:
    partition = build_synthetic_partition(records_per_client=3, evaluation_records=2, seed=seed)
    operating_points = [point.to_record() for point in build_operating_points()]
    manifest = ArtifactManifest(
        artifact_id="synthetic-contract-evidence",
        path="planning/synthetic_contract_evidence.json",
        status="synthetic",
        sha256=None,
        provenance={
            "source_profile_id": "synthetic-only",
            "partition_id": f"synthetic-partition-seed-{seed}",
            "config_revision": "local-synthetic",
            "seed": seed,
            "created_by": "local-contract-runner",
        },
    )
    validate_artifact_manifest(manifest)
    return {
        "project": "PrivacyFL-DP",
        "status": "synthetic",
        "scope": "local synthetic contract only",
        "seed": seed,
        "client_count": len(partition.client_shards),
        "evaluation_count": len(partition.evaluation_ids),
        "operating_labels": [point["label"] for point in operating_points],
        "total_epochs": TOTAL_EPOCHS,
        "measured_epsilon": None,
        "measured_auc": None,
        "artifact_manifest": {
            "artifact_id": manifest.artifact_id,
            "path": manifest.path,
            "status": manifest.status,
            "sha256": manifest.sha256,
            "provenance": dict(manifest.provenance),
        },
        "warnings": [
            "Synthetic contract evidence is not a privacy guarantee.",
            "No dataset, model, training, evaluation, Opacus accounting, or clinical metric was used.",
        ],
    }


def write_synthetic_evidence(path: Path, seed: int = 17) -> dict[str, Any]:
    record = build_synthetic_evidence(seed=seed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description="Write sanitized synthetic contract evidence.")
    parser.add_argument(
        "--output",
        default="planning/synthetic_contract_evidence.json",
        help="Project-local JSON output path.",
    )
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()
    output = Path(args.output)
    if output.is_absolute() or ".." in output.parts:
        raise SystemExit("output must be a project-relative path")
    record = write_synthetic_evidence(output, seed=args.seed)
    print(json.dumps({"output": str(output), "status": record["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
