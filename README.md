# Signal Orchestration Lab

![Hero](https://raw.githubusercontent.com/mizcausevic-dev/signal-orchestration-lab/main/screenshots/01-hero-v2.svg)

## Executive Summary

Signal Orchestration Lab is a Python + FastAPI backend that
ingests cross-functional operating signals, models their dependencies, and
routes them into coordinated response plans. It is designed to feel like the
infrastructure brain behind growth systems, briefing surfaces, and executive
control rooms.

## Why It Matters

This repo demonstrates:

- Python backend breadth alongside the broader TypeScript portfolio
- FastAPI and Pydantic for production-style API design
- Pandas-backed pressure scoring and normalization
- orchestration logic that respects dependency chains instead of flat issue lists
- a backend architecture that feels operational, not academic

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3.11+-111827?style=for-the-badge&logo=python&logoColor=FFD54F&labelColor=111827&color=1F6FEB)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Orchestration-111827?style=for-the-badge&logo=fastapi&logoColor=44E1B6&labelColor=111827&color=0F766E)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Models-111827?style=for-the-badge&logo=pydantic&logoColor=F9A8D4&labelColor=111827&color=7C3AED)](https://docs.pydantic.dev/)
[![Pandas](https://img.shields.io/badge/Pandas-Scoring-111827?style=for-the-badge&logo=pandas&logoColor=F4E7B3&labelColor=111827&color=4338CA)](https://pandas.pydata.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Tested-111827?style=for-the-badge&logo=pytest&logoColor=FBBF24&labelColor=111827&color=7C2D12)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-111827?style=for-the-badge&logo=opensourceinitiative&logoColor=E5E7EB&labelColor=111827&color=84CC16)](https://opensource.org/license/mit)

## Overview

| Area | What it shows |
| --- | --- |
| Signal modeling | Revenue, growth, ops, security, AI, and customer signals modeled as dependency-aware nodes |
| Orchestration logic | Pressure scoring, deadline weighting, and dependency-aware sequence ranking |
| Graph outputs | Explicit upstream and downstream relationships for escalation planning |
| API surface | FastAPI endpoints for list, detail, graph analysis, orchestration analysis, and dashboard summary |
| Operational framing | Backend decisioning that supports executive reviews and control-plane products |

## Architecture

```mermaid
flowchart LR
  P["Signal nodes"] --> V["Pydantic validation"]
  V --> F["Pandas pressure frame"]
  F --> O["Dependency ordering"]
  O --> R["Routed actions"]
  O --> G["Graph edges"]
```
```

## Sample Request

```json
{
  "orchestration_id": "orch-demo",
  "scenario_name": "Northstar executive pressure map",
  "environment": "production",
  "nodes": [
    {
      "signal_id": "rev-coverage",
      "lane": "revenue",
      "title": "Pipeline coverage compression",
      "owner": "Revenue Operations",
      "metric": "coverage",
      "current_value": 2.1,
      "target_value": 3.0,
      "confidence": 0.86,
      "severity": "critical",
      "due_in_days": 8,
      "dependencies": ["growth-attribution", "ops-routing"],
      "note": "Coverage dip is being amplified by poor attribution confidence and delayed routing."
    }
  ]
}
```

## Sample Response

```json
{
  "status": "coordinated",
  "score": 61,
  "orchestration_headline": "Northstar executive pressure map should anchor on pipeline coverage compression before downstream pressure compounds.",
  "pressure_clusters": [
    "Revenue pressure: 1 linked signals",
    "Growth pressure: 1 linked signals"
  ],
  "routed_actions": [
    {
      "title": "Coordinate around pipeline coverage compression",
      "owner": "Revenue Operations",
      "lane": "revenue",
      "severity": "critical",
      "sequence_rank": 1,
      "due_in_days": 8,
      "rationale": "Pipeline coverage compression carries 2 downstream dependencies and pressure score 67.8."
    }
  ]
}
```

## Screenshots

### Hero
![Hero](https://raw.githubusercontent.com/mizcausevic-dev/signal-orchestration-lab/main/screenshots/01-hero-v2.svg)

### Orchestration Graph
![Graph](https://raw.githubusercontent.com/mizcausevic-dev/signal-orchestration-lab/main/screenshots/02-graph-v2.svg)

### Routed Actions
![Actions](https://raw.githubusercontent.com/mizcausevic-dev/signal-orchestration-lab/main/screenshots/03-actions-v2.svg)

### Validation Proof
![Proof](https://raw.githubusercontent.com/mizcausevic-dev/signal-orchestration-lab/main/screenshots/04-proof-v2.svg)

## Setup

```powershell
Set-Location "C:\Users\chaus\dev\repos\signal-orchestration-lab"
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install .[dev]
uvicorn app.main:app --reload
```

Open:

- API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Validation

```powershell
Set-Location "C:\Users\chaus\dev\repos\signal-orchestration-lab"
python -m pytest
python -m compileall app tests
```

## Portfolio Links

- [Kinetic Gain](https://kineticgain.com/)
- [LinkedIn](https://www.linkedin.com/in/mirzacausevic)
- [Skills / Portfolio](https://mizcausevic.com/skills/)
- [Medium](https://medium.com/@mizcausevic)
- [GitHub](https://github.com/mizcausevic-dev)
