# Project 1 — 8-Puzzle Solver (A* Search)

This folder contains Project 1 for CAI 4002 (Intro to AI). The assignment implements an 8-puzzle (general N-puzzle) solver using the A* search algorithm with the Manhattan distance heuristic.

## Overview

- Problem: Solve the sliding-tile puzzle (N-puzzle). The blank tile is represented with `0` and tiles are numbered `0..(N-1)` where the goal state is the ordered sequence `0,1,2,...` in row-major order.
- Algorithm: A* search with f(n) = g(n) + h(n), where g(n) is the cost so far (number of moves) and h(n) is the Manhattan distance heuristic.

## Files in this directory

- `hw1.py` — reference implementation of the solver (A* with Manhattan distance). Exposes `solveSlider(size: int, grid: List[int]) -> List[int]`.
- `studentFile.py` — student's submitted implementation (same API as `hw1.py`).
- `graderScript.py` — grading harness used by instructors/TAs. It loads the student's file, runs the `solveSlider` function on inputs from `exampleInputs.jsonlist` (or `gradedInputs.jsonlist`), and compares outputs to `exampleOutputs.txt` (or `gradedOutputs.txt`).
- `exampleInputs.jsonlist` — example input cases (one JSON object per line).
- `exampleOutputs.txt` — expected outputs for the example inputs (one JSON object per line, with an `ans` field).
- `exampleOutputs.txt` — sample outputs used by the grader.
- `exampleInputs.jsonlist` — sample inputs used by the grader.
- `exampleOutputs.txt` — (duplicate named entries above — keep the files listed in your repo as-is).

## Usage

Prerequisites:

- Python 3.8+ (the code uses standard library only)

Run the solver manually (example):

```powershell
python -c "from studentFile import solveSlider; print(solveSlider(3, [1,2,3,4,5,6,7,8,0]))"
```

Run the grader on the example inputs:

```powershell
python graderScript.py
```

Notes on the grader:

- The grader expects the student file to define `solveSlider(size: int, grid: List[int]) -> List[int]`.
- For each test case the solver should return a list of integers representing the tile numbers moved in order. The grader applies these moves to the board and verifies whether the board reaches the goal state.
- `maxruntime` in `graderScript.py` limits the allowed runtime per test (default 1 second).

## Input / Output format

- Each input JSON object contains the fields required by `solveSlider`. Example input line (in `exampleInputs.jsonlist`):

```json
{"size": 3, "grid": [1,2,3,4,5,6,7,8,0]}
```

- The solver must return a Python `list` of integers, where each integer is the tile number (not an index) the solver chooses to move at each step. The grader will validate each move.

## Example

- Start state: [1,2,3,4,5,6,7,8,0] (already solved). The solver should return `[]`.
- A non-trivial example will produce a sequence like `[8,5,2,...]` (tile numbers moved to shift the blank).

## Tips & Troubleshooting

- If the grader reports your function is missing, ensure the file name (`studentFile.py`) and function name (`solveSlider`) match the constants at the top of `graderScript.py`.
- If your solution is correct but times out, consider more efficient bookkeeping (avoid revisiting states, use a proper priority queue, and store g(n) per node instead of incrementing a shared counter incorrectly).
- In `hw1.py` watch out: incrementing `gn` in the loop without copying it will corrupt g values for other nodes. Use a local variable for child g-value (e.g., child_g = parent_g + 1) when pushing to the queue.

## Author / License

Author: Joshua Maharaj (U24183946)

This repository is for coursework. Check your university policies before sharing publicly.
