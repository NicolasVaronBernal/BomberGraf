# Graph-Based Decision Support System (DSS)

This project implements a **Decision Support System (DSS)** based on **Graph Theory** to navigate a dynamic maze. The software helps players find the most efficient routes by calculating the balance between physical distance and environmental risk (threats) in real-time.

## Mathematical Foundations

* **Grid Graphs:** The environment is modeled as a graph $G=(V, E)$ where nodes represent cells and edges represent connections.
* **Induced Subgraphs:** Static obstacles are handled by removing nodes ($G.remove\_node(v)$), ensuring the graph topology reflects the maze.
* **Menger’s Theorem:** Used to ensure path connectivity, guaranteeing that the generated maze is always solvable with at least one alternative route.
* **Dijkstra’s Algorithm:** Optimizes weighted paths by calculating the minimal cost $\min \sum w$, where weights $w$ represent movement cost plus proximity to mobile threats.

## Technical Features

* **Built with Python & NetworkX:** High-performance graph processing.
* **Stochastic Dynamics:** Enemies move with a 70% probability, forcing the algorithm to recalculate the optimal path every turn.
* **Visual DSS:** Provides a "Top 3" path analysis, classifying routes by color (White, Green, Yellow) based on their risk-adjusted cost.
* **Algorithmic Trace:** Displays adjacency matrices and the step-by-step relaxation process of Dijkstra's algorithm.

## Installation

Ensure you have Python installed, then install the required library:

```bash
pip install networkx

```

## How to Run

Run the main script from your terminal:

```bash
python main.py

```

* **Controls:** Use `w`, `a`, `s`, `d` to move.
* **Analysis:** The terminal will display the adjacency matrices and the Dijkstra step-by-step trace before every move.

## Code Overview

The system follows an Object-Oriented approach:

1. **Topological Modeling:** Transforms the $10 \times 10$ board into a graph and validates maze solvency.
2. **Stochastic Engine:** Manages player inputs and updates enemy positions based on random probabilities.
3. **Optimization Engine:** Computes three distinct paths. It enforces a strict rule where the 3rd path must have a weight at least 5 units higher than the 2nd, highlighting the difference between "safe" and "risky" routes.
4. **Visual Interface:** Uses ANSI escape codes to render the map and the mathematical trace in the terminal.

---

*Developed as a practical application of Discrete Mathematics.*
