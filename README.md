# Oedipus

```
oedipus-puzzle/
├── pyproject.toml
├── game.html                    playable puzzle, opens in a browser
├── assets/                      the reference picture the solved puzzle shows
├── data/                        generated output, not tracked
├── temp/graph_theory.py         scratchpad: code is written here, then moves into oedipus/
├── scripts/                     runnable entry points
│   └── demo_render.py
├── tests/
│   ├── conftest.py              helpers only tests need
│   ├── test_board.py
│   ├── test_parity.py
│   └── test_bfs.py
└── oedipus/
    ├── core/                    pure logic, imports nothing of ours
    │   ├── board.py             Board, BLANK, find_blank, swap, neighbors, degree, goal
    │   ├── parity.py            inversions, parity_class, reachable, random_board
    │   └── graph.py             explore
    ├── solvers/                 exact solving, no learning
    │   ├── bfs.py               distances_from, optimal_path
    │   └── astar.py             A*, Manhattan, pattern databases
    ├── env/
    │   ├── puzzle_env.py        Gymnasium environment
    │   └── scramble.py          start-state generators
    ├── agents/
    │   ├── tabular.py           value iteration, Q-learning
    │   └── dqn.py               deep Q-network
    ├── render/
    │   ├── text.py              render_text, render_row
    │   ├── tiles.py             load_reference, cut_tiles, styles
    │   ├── board.py             render_board
    │   └── anim.py              save_gif
    ├── eval/
    │   └── metrics.py           optimality gap, solve rate
    └── analysis/
        └── markov.py            transition matrix, stationary distribution
```

Dependency direction:

```
core            <- solvers, env, render
core, solvers   <- eval
core, env       <- agents
everything      <- scripts
```

Nothing points back down.
