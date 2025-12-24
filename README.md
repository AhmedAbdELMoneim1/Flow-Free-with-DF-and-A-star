# Flow Free Solver with Depth-First Search and A*

An intelligent AI solver for the popular Flow Free puzzle game, implementing both Depth-First Search with optimizations and A* search algorithm with custom heuristics.

## 🎮 About Flow Free

Flow Free is a puzzle game where you connect matching colored dots on a grid. The challenge is to connect all pairs while filling every square on the board, with paths not allowed to cross or overlap.

## 🧠 Problem Formulation

- **State**: The entire board configuration
- **Actions**: Extend one color path by one step in any valid direction
- **Goal**: All color pairs connected AND the entire board is filled
- **Constraint**: Every square must contain exactly one color (no empty squares, no wasted paths)

## 🔍 Search Algorithms Implemented

### 1. Depth-First Search (DFS)
Basic DFS implementation with backtracking to explore possible path configurations.

**Performance:**
- 6×6 boards: Solved in ~783 steps
- 8×8 boards: Solved in ~16,364 steps  
- 10×10 boards: Cannot solve efficiently (too many states)

### 2. A* Search with Optimizations
Enhanced A* algorithm with intelligent heuristics and pruning techniques for significantly better performance.

**Key Optimizations:**
- **Dead-end Detection**: Identifies squares that would become unreachable or create wasted space
- **Minimum Expansion Heuristic**: Prioritizes moves toward squares with fewer expansion options
  - Squares with 3 possible expansions: weight = 1
  - Squares with 2 possible expansions: weight = 2  
  - Squares with 1 possible expansion: weight = 3
- **Direction Preference**: Evaluates nearest valid directions first to reduce search space

**Performance:**
- 8×8 boards: Solved in ~110 steps 
- 10×10 boards: Solved in ~20,000 steps

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.10+
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AhmedAbdELMoneim1/Flow-Free-with-DF-and-A-star.git
cd Flow-Free-with-DF-and-A-star
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

Run the solver:
```bash
streamlit run main.py
```

Configure puzzle parameters in `configurations.py` to test different board sizes and color configurations.

## 📁 Project Structure

```
Flow-Free-with-DF-and-A-star/
├── DF_A_Star.py          # Core search algorithms implementation
├── configurations.py      # Board configurations and test cases
├── main.py               # Main entry point
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```
