# Project 17 Evidence Ledger

## Current Evidence

| Evidence | Status | Interpretation |
|---|---|---|
| Local synthetic package under `src/privacyfl_dp/` | synthetic | Contract checks only; not a real FL or DP runtime |
| Local tests under `tests/` | synthetic | `23 passed in 0.15s` for local contracts |
| `planning/synthetic_contract_evidence.json` | synthetic | Sanitized evidence; measured fields are null |
| Kaggle notebook | planned | JSON-valid and unexecuted; no runtime evidence |
| NIH ChestX-ray14 data | not-created | Blocked pending approval |
| Model weights/checkpoints | not-created | No model artifacts exist |
| Measured epsilon | not-created | No Opacus run occurred |
| Measured AUC/utility | not-created | No training or evaluation occurred |
| Public-safe export | synthetic | Contains only allowed local synthetic artifacts |

## Exact Verified Result

Command: `python -m pytest tests -q`

Result: `23 passed in 0.15s`

Exit code: `0`

Fresh closeout rerun on 2026-09-16:

- Command: `python -m pytest tests -q`
- Result: `23 passed in 0.45s`
- Final verification rerun: `23 passed in 0.14s`
- Exit code: `0`
- JSON/notebook parse: PASS; `12` cells, `9` code cells, `0` executed code cells.
- Public export scans: exclusion, internal residue, private path, secret, and data/model/checkpoint checks passed.
- Git whitespace check: not applicable because this folder is not a Git repository.

## Negative Evidence

No NIH data, patient data, model weights, Opacus runtime, Flower runtime, GPU work, heavy CPU work, Kaggle run, package installation, API call, commit, or push occurred during this closeout.
