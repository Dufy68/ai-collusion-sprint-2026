# AI Collusion Research Sprint 2026 — Track 1.5

Exploratory continuous double-auction experiments with Qwen/Qwen2.5-7B-Instruct. This repository contains sprint-written launchers and independent analysis, synthetic experiment traces, and a patch against the official starter.

## Scope and findings

Nine completed 15-round sessions compare three conditions at seeds 0, 1, and 2: seller communication with no profit pressure; communication with profit pressure; and no communication with profit pressure. Three buyers and three sellers participate in each session. A separate smoke test and incomplete/setup attempts are retained and indexed in `RUN_INDEX.json`.

**We did not establish a sustained high-price positive control. These runs do not demonstrate an effective anti-collusion intervention.** Price changes alone do not identify collusion. The study is an exploratory pilot with three sessions per condition, one model, short horizons, and no inferential claims. Seeds do not guarantee deterministic GPU generation; model weights were not pinned to a revision.

## Reproduce the recorded analysis (no cloud access required)

Use Python 3.9 or newer. The two audit scripts use the standard library:

```sh
python analyze_sprint15.py
python audit_sprint15_traces.py
```

For comparison figures, use Python 3.10+ in a virtual environment:

```sh
python -m pip install -r requirements-analysis.txt
python compare_sprint15.py
python compare_nocomms.py
```

Outputs are written to `sprint15_analysis/`. See `TRACE_AUDIT.md`, `BASELINE_FINDINGS.md`, `PRESSURE_FINDINGS.md`, and `NOCOMMS_FINDINGS.md` there. `PACKAGE_TEST_RESULTS.md` records earlier teammate-copy verification. Tiny floating-point differences across Python versions are expected.

## Re-run simulations (optional, incurs compute costs)

The official starter source is fetched separately rather than re-licensed or redistributed here:

```sh
python bootstrap_upstream.py
cd llm-agent-collusion
uv sync
cd ..
```

Read the upstream project README and `EXPERIMENT_ENVIRONMENT.json` before running. Set up and authenticate the official Modal Python client separately. The launchers expect the experiment interpreter at `llm-agent-collusion/.venv/bin/python` and an authenticated Modal account. They download model weights and use a GPU; costs depend on current pricing and runtime. The original experiment used Modal 1.2.6 for the launcher environment and its environment snapshot is included. `experiment-requirements.txt` records the experiment environment rather than guaranteeing portability across all Python versions.

`sprint15_nocomms.py` and `sprint15_pressure_seed2.py` include explicit app shutdown. Earlier smoke/baseline/retry launchers are preserved as historical experiment records; inspect lifecycle handling before using them. New runs create timestamped result directories; preserve the published traces before aggregating new data.

## Provenance and work attribution

- Pre-existing third-party work: [Apart/Poseidon official starter](https://github.com/poseidon-research/collusion_hackathon), baseline commit `d585a7b3be50366cc2bdf5789bf8add5890b2abd`, including the auction simulator and utilities. Their source and model retain their respective authorship and terms. No new blanket license is assigned to those materials.
- Pre-existing participant work: none reused, as confirmed by the participant. Agentic AI coursework was background only.
- Work completed during the sprint: Modal launchers; numeric bid/ask compatibility patch; the recorded runs; independent trace/metric audit; descriptive comparisons and figures. AI assistance was used for coding, debugging, analysis, and drafting; authors remain responsible for verification.
- `SPRINT_CODE_CHANGES.patch` converts numeric strings to finite floating-point prices in the starter market code. `bootstrap_upstream.py` restores the pinned starter and applies this patch.

The report draft and author placeholders are excluded from this code release. This repository is not evidence of report submission or final billing reconciliation.

## Limitations and ethical considerations

This toy market uses synthetic valuations and agents; results do not establish real-world market behavior or generalize across models. The audit recomputes metrics from trajectories because some upstream summary metrics have interpretation/implementation limitations (documented in the audit). The required positive control was not achieved, limiting intervention conclusions.

Multi-agent coordination experiments can inform both detection and collusion strategies. These artifacts are intended for reproducibility and safety evaluation in a sandbox. No real customers, market accounts, or trading systems were used. Credentials, local environments, and private cloud server logs are excluded. Do not interpret synthetic dialogue as allegations about people or firms.
