# Route / Control

**A driver-aware last-mile routing and dispatch decision system built on Amazon and MIT's public research benchmark.**

Route / Control turns a classic route-optimization exercise into an operating decision: compare drive time, timed-package service and route coherence before dispatch. It learns driver zone-sequencing preferences from historical routes, combines them with a constraint-aware local search, and exposes both the aggregate result and routes that still need intervention.

## Verified result

On a separate 13-route public application cohort with 2,038 stops and 3,129 packages, the hybrid policy:

- reduced simulated drive time by **85.2 minutes (2.8%)** versus directed nearest neighbour;
- preserved **100% on-time service for 210 timed packages**;
- reduced zone re-entry from **332 to 0**.

Against the retrospective observed-driver reference, the hybrid was 25.6 minutes (0.9%) slower across the cohort, while improving simulated timed-package adherence from 99.5% to 100% and reducing re-entry from 26 to 0. The observed sequence remains a reminder that public fields do not capture all tacit driver knowledge.

These are retrospective simulation results—not production savings, a live deployment, or challenge leaderboard performance.

## What is inside

```text
artifacts/              Verified data-quality, model and evaluation outputs
dashboard/              Responsive React + Vite dispatch control tower
data/                   Source manifest and generated route-policy metrics
docs/                   Decision contract, model card, claims and validation
notebooks/              Executed reader-facing analysis
scripts/                Data acquisition, pipeline, notebook and browser QA
src/route_control/      Routing, simulation and evaluation package
tests/                  Deterministic source and claim checks
```

## Data source and split

The project uses the [2021 Amazon Last Mile Routing Research Challenge Dataset](https://registry.opendata.aws/amazon-last-mile-challenges/), introduced by Merchán et al. and supported by MIT Center for Transportation & Logistics.

- Training: route fields and observed sequences for 6,112 historical routes.
- Application benchmark: the separate 13-route `model_apply_inputs` cohort.
- Retrospective scoring: the matching actual sequences from `model_score_inputs`.
- Public dataset license: CC BY-NC 4.0. Raw source files are downloaded locally and never committed.

The dataset contains anonymized/obfuscated route, stop, package and directed travel-time data. The code in this repository is MIT licensed; that license does not change the dataset's license.

## Reproduce

Python 3.11+ is required.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python scripts\download_data.py
python scripts\run_pipeline.py
python scripts\build_notebook.py
python -m pytest -q
```

Execute the notebook with Jupyter or `nbclient`. The committed notebook is already executed and its outputs are traceable to `artifacts/evaluation.json`.

Run the control tower:

```powershell
cd dashboard
pnpm install
pnpm dev
```

## Method in one view

1. Learn transition and relative order preferences across historical zone sequences.
2. Create learned-order and time-window-priority zone candidates.
3. Sequence stops using directed travel time plus a soft service-window penalty.
4. Improve stop order and whole-zone order without permitting zone re-entry.
5. Compare against nearest neighbour and the retrospective observed sequence.

See [model card](docs/model-card.md), [decision contract](docs/decision-contract.md), [approved portfolio claims](docs/portfolio-claims.md), and [validation report](docs/validation-report.md).
