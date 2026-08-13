# Agent / Proof

**A release-readiness and failure-diagnostics system for tool-using AI agents.**

Agent / Proof asks a more useful question than “which model tops the leaderboard?”: **which model-domain combination is dependable enough to release, what breaks under repetition, and where should a team intervene first?**

It reconstructs repeated-task reliability, cost, latency, tool behaviour and evaluator failure signals from 3,336 official historical trajectories across three models and three operational domains. No model API was called.

![Agent Proof dashboard](docs/qa/desktop-render.png)

## The decision in one screen

The default GPT-4.1 / telecom cohort passes 34.2% of single sampled trials, but only 19.3% of tasks remain successful across all four trials. Half of the benchmark tasks always fail, and 99.0% of failed runs carry a missing-expected-action diagnostic. That combination produces a transparent **HOLD** release gate and a concrete intervention target.

The dashboard supports:

- model and domain cohort selection;
- Pass¹–Pass⁴ repeatability curves;
- always-pass, unstable and always-fail task segmentation;
- four-trial task inspection with cost, latency, tool calls and action matches;
- deterministic evaluator-based failure diagnostics;
- action-family and cost-per-success comparisons.

## Evidence-backed findings

| Cohort | Pass¹ | Pass⁴ | Always fail | Reported cost / success |
|---|---:|---:|---:|---:|
| GPT-4.1 · telecom | 34.2% | 19.3% | 50.0% | $0.32 |
| o4-mini · telecom | 42.1% | 26.3% | 40.4% | $0.22 |
| Claude 3.7 Sonnet · telecom | 49.3% | 25.4% | 29.8% | $1.18 |
| Claude 3.7 Sonnet · retail | 78.7% | 59.6% | 7.0% | $0.42 |

These are descriptive results for the pinned historical trajectory cohort—not claims about current or production model performance.

## Reproduce

Prerequisites: Python 3.11+, Node.js 20+, Git and pnpm.

```bash
python scripts/download_data.py
python -m pip install -e ".[dev]"
python scripts/run_pipeline.py
python -m pytest
cd dashboard
pnpm install
pnpm build
```

The source manifest records the upstream revision. Processed data is rebuilt locally and excluded from Git; the compact dashboard evidence is committed at `dashboard/public/data/results.json`.

## Repository map

```text
artifacts/                 decision outputs and validation evidence
dashboard/                 responsive React evidence console
data/                      source manifest and data documentation
docs/                      contract, model card, claim controls and visual QA
notebooks/                 executed decision analysis
scripts/                   acquisition, pipeline and browser QA
src/agent_lab/             metric and diagnostic logic
tests/                     deterministic validation tests
```

## Method and limits

- Passᵏ is the average task-level probability that all `k` trials sampled without replacement succeed, computed from four repeated trials.
- Failure categories follow a documented precedence over official evaluator fields; they are inspection cues, not human-reviewed causal diagnoses.
- The release gate is a portfolio decision rule: release at Pass⁴ ≥ 70%, monitor at 50–70%, hold below 50%. It is not an upstream benchmark standard.
- Model prices, prompts and benchmark tasks may change. Re-run on a current, representative evaluation set before any deployment decision.

See the [decision contract](docs/decision-contract.md), [model card](docs/model-card.md), [approved claims](docs/approved-claims.md) and [validation report](artifacts/validation-report.md).

## Source and license

Trajectory data comes from the maintained [Sierra Research tau2-bench repository](https://github.com/sierra-research/tau2-bench). The repository code is MIT licensed; review upstream dataset and benchmark terms before reuse. This project code is MIT licensed.
