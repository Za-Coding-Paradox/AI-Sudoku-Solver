# AI Sudoku Solver

A constraint satisfaction problem (CSP) solver for Sudoku puzzles, implementing **AC-3 arc consistency** preprocessing combined with **backtracking search** and **forward checking** to efficiently solve puzzles of any difficulty.

---

## Table of Contents

- [Overview](#overview)
- [Algorithm Design](#algorithm-design)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Output](#output)
- [Performance Metrics](#performance-metrics)
- [Input Format](#input-format)

---

## Overview

This solver models Sudoku as a **Constraint Satisfaction Problem (CSP)**, where:

- **Variables** — Each of the 81 cells on the board `(row, col)`
- **Domains** — The set of possible digit values `{1–9}` for each cell (pre-filled cells have a singleton domain)
- **Constraints** — No two cells in the same row, column, or 3×3 box may share the same digit

The solver applies two stages of reasoning: a **preprocessing** phase using AC-3 to prune domains before search, followed by a **recursive backtracking search** augmented with forward checking and the MRV heuristic to navigate remaining ambiguity.

---

## Algorithm Design

### Stage 1 — AC-3 Preprocessing

Before any search begins, the **AC-3 (Arc Consistency 3)** algorithm propagates constraints across the board. For every pair of constrained variables `(Xi, Xj)`, it removes values from `Xi`'s domain that have no compatible value in `Xj`'s domain. This prunes the search space significantly, often solving easy puzzles outright.

If any domain is reduced to empty during this phase, the board is declared unsolvable immediately.

### Stage 2 — Backtracking Search with Forward Checking

If AC-3 alone does not resolve the puzzle, the solver proceeds with **recursive backtracking**:

- **Variable Selection (MRV Heuristic)** — At each step, the unassigned variable with the fewest remaining domain values is selected first (*Minimum Remaining Values*). This targets the most constrained cell, reducing branching early.

- **Forward Checking** — After each assignment, the assigned value is immediately removed from the domains of all unassigned neighboring cells. If any neighbor's domain becomes empty, the assignment is abandoned without further recursion.

- **Backtracking** — When a dead end is reached, the solver restores all domain changes made during forward checking and tries the next candidate value.

---

## Project Structure

```
AI_Sudoku_Solver/
├── main.py                 # Entry point: reads input, orchestrates solving, prints results
├── linux_runner.sh         # Shell script to run the full test suite on Linux/macOS
├── windows_runner.bat      # Batch script to run the full test suite on Windows
├── src/
│   ├── __init__.py
│   ├── csp.py              # SudokuCSP class: variables, domains, neighbors, consistency check
│   └── algorithms.py       # AC-3, forward checking, and backtracking search
└── data/
    ├── __init__.py
    ├── easy.txt
    ├── medium.txt
    ├── hard.txt
    └── expert.txt
```

### Module Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | CLI interface, file I/O, result display, and solver orchestration |
| `src/csp.py` | CSP model — domain initialization, constraint graph, consistency checks |
| `src/algorithms.py` | AC-3, `revise()`, forward checking, and recursive backtracking |
| `data/*.txt` | Puzzle input files, one per difficulty level |

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies — the solver uses the Python standard library only

### Installation

```bash
git clone https://github.com/your-username/AI_Sudoku_Solver.git
cd AI_Sudoku_Solver
```

---

## Usage

### Solve a Single Puzzle

```bash
python main.py data/easy.txt
python main.py data/medium.txt
python main.py data/hard.txt
python main.py data/expert.txt
```

### Run the Full Test Suite

**Linux / macOS:**
```bash
chmod +x linux_runner.sh
./linux_runner.sh
```

**Windows:**
```bat
windows_runner.bat
```

### Solve a Custom Puzzle

Create a `.txt` file in the format described below and pass it as an argument:

```bash
python main.py path/to/your_puzzle.txt
```

---

## Output

A successful run prints the solved board alongside performance metrics:

```
Processing: data/hard.txt
Running AC-3 inference...
Executing Backtracking Search with Forward Checking...

Solution Found:
-------------
|534|678|912|
|672|195|348|
|198|342|567|
-------------
|859|761|423|
|426|853|791|
|713|924|856|
-------------
|961|537|284|
|287|419|635|
|345|286|179|
-------------

--- Performance Metrics ---
Backtrack Calls:    142
Backtrack Failures: 38
---------------------------
```

---

## Performance Metrics

The solver tracks two counters throughout the search:

| Metric | Description |
|---|---|
| **Backtrack Calls** | Total number of times the recursive `backtrack()` function was invoked. Reflects the total nodes explored in the search tree. |
| **Backtrack Failures** | Number of times a branch was fully exhausted with no valid assignment. A lower value indicates more effective pruning by AC-3 and forward checking. |

On well-constrained puzzles, AC-3 alone may reduce domains enough that backtracking requires very few calls. On adversarial or near-minimal puzzles, the MRV heuristic and forward checking keep the failure count manageable.

---

## Input Format

Puzzle files must be a plain-text 9×9 grid with one row per line. Use `0` to represent an empty cell.

**Example (`easy.txt`):**
```
530070000
600195000
098300060
800060003
400803001
700020006
060000280
000419005
000080079
```

Requirements:
- Exactly 9 lines
- Exactly 9 characters per line
- Characters must be digits `0–9`
- No spaces, commas, or separators
