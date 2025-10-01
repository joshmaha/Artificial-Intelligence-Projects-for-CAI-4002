# Project 2 — 3D Tic-Tac-Toe AI (Alpha-Beta / Minimax)

This folder contains Project 2 for CAI 4002. The project implements a 3D Tic-Tac-Toe game and several AI agents that play the game using minimax / alpha-beta search and heuristics.

## Overview

- Game: 3D Tic-Tac-Toe on an N x N x N board (implemented up to size 5).
- AIs: Heuristic-based players that use alpha-beta pruning and forward pruning (move ordering) to choose moves.

## Files

- `tdTTT.py` — core game implementation (TicTacToe3D class). Exposes board, legal moves, make_move, check_winner, and utility functions.
- `hw2.py` — simulation script that uses alpha-beta search and two heuristics to run games and collect statistics.
- `hw2updated.py` — improved AI class (`playerAI`) with forward pruning, evaluation heuristics, minimax, and full simulation harness (`full_sim`).
- `HW2 template.ipynb` — notebook template (if present) for interactive experimentation.

## Requirements

- Python 3.8+
- No external pip dependencies (uses only standard library and `copy`, `typing`).

## How to run

Run a single simulation from `hw2.py` or `hw2updated.py`:

```powershell
# Run an example simulation (prints results)
python Project2\hw2.py

# Or run the updated simulation with more options
python -c "from Project2.hw2updated import full_sim; full_sim(10, size=5, max_depth=2, fw_prune=0.3)"
```

Examples and notes:
- `full_sim(num_games, size, max_depth, fw_prune)` runs `num_games` and reports win rates. `fw_prune` is a fraction (0-1) of moves to keep when forward-pruning.
- To experiment interactively, import `TicTacToe3D` from `tdTTT.py` in a Python REPL or notebook.

## Design notes & tips

- The AI uses forward pruning to limit branching (keeps top-k moves by heuristic score). Tune `max_depth` and `fw_prune` to trade off runtime vs. playing strength.
- `tdTTT.TicTacToe3D` supports board sizes 1..5. Larger sizes increase branching rapidly.

## Author

Joshua Maharaj
