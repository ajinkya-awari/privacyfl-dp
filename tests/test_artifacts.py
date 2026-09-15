import pytest

from privacyfl_dp.artifacts import ArtifactManifest, validate_artifact_manifest


def valid_manifest(**overrides):
    data = {
        "artifact_id": "synthetic-contract-record",
        "path": "planning/synthetic_contract_evidence.json",
        "status": "synthetic",
        "sha256": "a" * 64,
        "provenance": {
            "source_profile_id": "synthetic-only",
            "partition_id": "synthetic-partition-seed-17",
            "config_revision": "local-synthetic",
            "seed": 17,
            "created_by": "local-contract-runner",
        },
    }
    data.update(overrides)
    return ArtifactManifest(**data)


def test_valid_synthetic_artifact_manifest_is_accepted():
    validate_artifact_manifest(valid_manifest())


def test_path_traversal_is_rejected():
    with pytest.raises(ValueError, match="path traversal"):
        validate_artifact_manifest(valid_manifest(path="../outside.json"))


def test_raw_data_model_and_checkpoint_paths_are_rejected():
    for path in ("data/raw.csv", "models/model.pt", "checkpoints/run.ckpt"):
        with pytest.raises(ValueError, match="artifact path"):
            validate_artifact_manifest(valid_manifest(path=path))


def test_malformed_sha256_is_rejected():
    with pytest.raises(ValueError, match="sha256"):
        validate_artifact_manifest(valid_manifest(sha256="not-a-hash"))


def test_malformed_provenance_is_rejected():
    manifest = valid_manifest(provenance={"source_profile_id": "synthetic-only"})

    with pytest.raises(ValueError, match="provenance"):
        validate_artifact_manifest(manifest)
