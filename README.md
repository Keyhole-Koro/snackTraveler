# SnackTraveler: Self-Evolving Web Exploration Agent System

## Overview

SnackTraveler is a proof-of-concept system for a self-evolving web exploration agent. It uses evolutionary algorithms to discover and maintain a diverse population of strategies for web exploration.

This project demonstrates a hybrid approach combining:
- **MAP-Elites** for diversity preservation.
- A **Multi-Armed Bandit (Thompson Sampling)** for efficient strategy selection.
- **Multi-objective fitness evaluation (NSGA-II)** to assess strategies without manual weighting.

## Detailed Documentation

For a full breakdown of the project's architecture, components, and concepts, please refer to the detailed documentation in the `docs` directory.

- **[Project Overview](./docs/00_Project_Overview.md)**
- **[System Architecture](./docs/01_Architecture.md)**
- **[Data Models](./docs/02_Data_Models.md)**
- **[Evaluation Engine](./docs/03_Evaluation.md)**
- **[MAP-Elites Implementation](./docs/04_MAP_Elites.md)**
- **[Bandit Allocator](./docs/05_Bandit.md)**
- **[Execution Flow](./docs/06_Execution_Flow.md)**
- **[Usage Guide](./docs/07_Usage.md)**

## Quick Start

### Running the Simulation

From the project root (`snack/`), run:
```bash
python3 -m snackTraveler.main
```

### Running Tests

From the project root (`snack/`), run:
```bash
python3 -m unittest discover snackTraveler/tests
```