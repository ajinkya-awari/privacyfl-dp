# Kaggle Runbook - PrivacyFL-DP

This runbook prepares a later Kaggle session. It does not authorize data/model downloads, GPU training, provider calls, heavy CPU work, uploads, publication, or benchmark claims.

## Notebook

Use `notebooks/kaggle_privacyfl_dp.ipynb`.

## Rules

- Run cells manually, one at a time.
- Stop at the approval gate before real data, model downloads, providers, GPU training, or heavy CPU work.
- Do not assume `/kaggle/input` contains a specific dataset.
- Preserve evidence files; do not delete historical or failed evidence.
- Record every command, exit status, timestamp, and output path.
- Use only provider-free synthetic validation unless a human explicitly approves the real-data/runtime phase.

## Cell-by-Cell Sequence

1. Read the purpose, safety rules, and expected outputs.
2. Inspect the Kaggle environment and paths.
3. Inspect available input mounts without assuming dataset names.
4. Copy the uploaded source tree into `/kaggle/working/privacyfl_dp`.
5. Inspect the inactive dependency-installation cell; execute it only if dependency installation has explicit approval for this Kaggle session.
6. Restart the kernel only if an approved dependency installation was executed.
7. Run provider-free synthetic validation.
8. Inspect and preserve existing evidence files.
9. Stop at the approval gate.
10. Run optional approved runtime commands only after explicit approval, one cell at a time.
11. Summarize evidence and stop without uploading or publishing.

## Expected Evidence

The only safe default evidence is an environment/path inventory and synthetic validation output. Real dataset profiles, epsilon records, metrics, and figures remain blocked until approved.

<!-- 2026-08-28-session-pause -->

## Session Pause - 2026-08-28

The user will continue the remaining work on 2026-08-29. Until explicit implementation release is recorded, keep this file in planning/documentation mode: no source implementation, package installation, data/model download, training, evaluation, provider call, deployment, publication, commit, or push is authorized. Preserve all historical, synthetic, unverified, failed, and blocked evidence labels.