## Pathfinder Visualization

This project is a Python visualization tool for exploring how different pathfinding algorithms work in a grid-based environment. You can set start and end points, add barriers or weights, and then watch how the algorithm finds a path.

The interface is interactive and built using Pygame, and it includes support for multiple algorithms.

## Algorithms Used

- A* (A-Star): Uses a heuristic (Manhattan distance) and cost-so-far to find an optimal path.
- Dijkstra's Algorithm: A uniform-cost search that finds the shortest path without using a heuristic.
- Breadth-First Search (BFS): Explores all nodes at the current depth before moving to the next level.
- Bellman-Ford: Supports negative weights and detects negative cycles (listed as a button, may be in progress).

All algorithms are rule-based and use cost functions, queues, and priority queues to determine efficient paths. The final path is visually reconstructed once the goal is reached.

## How to Run It

### 1. Requirements

- Python 3.x
- Pygame

Install Pygame using pip:

pip install pygame

### 2. Run the Program

Navigate to the directory containing `main.py` and run:

python3 main.py

## Controls

- Left Click: Place start point, end point, or barriers
- Right Click: Remove barriers or reset tiles
- Shift + Click: Add weighted tiles (higher movement cost)
- Buttons at the top: Run a specific algorithm or reset the grid

## File Overview

- main.py: Contains the grid setup, visualization code, and algorithm implementations using Pygame

## Purpose

This project was created to help understand how classic pathfinding algorithms operate and to visualize their behavior. It serves as a useful starting point for anyone interested in artificial intelligence, algorithms, or game development.
