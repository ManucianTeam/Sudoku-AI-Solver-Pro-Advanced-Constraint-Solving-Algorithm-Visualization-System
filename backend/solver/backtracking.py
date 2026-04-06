"""
backtracking.py

Advanced Backtracking Solver for Sudoku using CSP techniques.

Features:
- MRV (Minimum Remaining Values)
- Degree Heuristic (tie-break)
- LCV (Least Constraining Value)
- Forward Checking
- AC-3 ready integration

Author: kennz_psix
"""

from typing import List, Set, Tuple, Optional
from copy import deepcopy

# Heuristics
from heuristics.mrv import find_mrv_with_tiebreak
from heuristics.degree import compute_degree
from heuristics.lcv import order_values_lcv

Board = List[List[int]]
Domains = List[List[Set[int]]]


# ---------------------------------------------------------------------------
# Utility: Constraint Check
# ---------------------------------------------------------------------------

def is_valid(board: Board, row: int, col: int, value: int) -> bool:
    """
    Check if placing value at (row, col) is valid.
    """

    # Row
    if any(board[row][i] == value for i in range(9)):
        return False

    # Column
    if any(board[i][col] == value for i in range(9)):
        return False

    # Subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == value:
                return False

    return True


# ---------------------------------------------------------------------------
# Domain Initialization
# ---------------------------------------------------------------------------

def initialize_domains(board: Board) -> Domains:
    """
    Initialize domains for all cells.
    """
    domains = [[set() for _ in range(9)] for _ in range(9)]

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                domains[r][c] = {
                    v for v in range(1, 10)
                    if is_valid(board, r, c, v)
                }
            else:
                domains[r][c] = {board[r][c]}

    return domains


# ---------------------------------------------------------------------------
# Forward Checking
# ---------------------------------------------------------------------------

def forward_check(domains: Domains, row: int, col: int, value: int) -> bool:
    """
    Remove 'value' from neighbors' domains.

    Returns False if any domain becomes empty.
    """

    for i in range(9):
        # Row
        if value in domains[row][i] and len(domains[row][i]) > 1:
            domains[row][i].discard(value)
            if not domains[row][i]:
                return False

        # Column
        if value in domains[i][col] and len(domains[i][col]) > 1:
            domains[i][col].discard(value)
            if not domains[i][col]:
                return False

    # Subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if value in domains[r][c] and len(domains[r][c]) > 1:
                domains[r][c].discard(value)
                if not domains[r][c]:
                    return False

    return True


# ---------------------------------------------------------------------------
# Backtracking Solver
# ---------------------------------------------------------------------------

def backtrack(
    board: Board,
    domains: Domains,
    steps: List[int]
) -> bool:
    """
    Core recursive backtracking function.

    Args:
        board: Sudoku board
        domains: domain grid
        steps: list used as mutable counter

    Returns:
        True if solved
    """

    # Check if solved
    if all(board[r][c] != 0 for r in range(9) for c in range(9)):
        return True

    # Select variable using MRV + Degree
    row, col = find_mrv_with_tiebreak(board, domains, compute_degree)

    # Try values using LCV ordering
    for value in order_values_lcv(board, domains, row, col):

        if is_valid(board, row, col, value):
            board[row][col] = value
            steps[0] += 1

            # Save state
            saved_domains = deepcopy(domains)

            # Forward checking
            if forward_check(domains, row, col, value):

                if backtrack(board, domains, steps):
                    return True

            # Undo (backtrack)
            board[row][col] = 0
            domains[:] = saved_domains

    return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def solve(board: Board) -> Tuple[bool, int]:
    """
    Solve Sudoku using advanced CSP backtracking.

    Returns:
        (solved: bool, steps: int)
    """

    domains = initialize_domains(board)
    steps = [0]

    success = backtrack(board, domains, steps)

    return success, steps[0]


# ---------------------------------------------------------------------------
# Debug / Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("Solving Sudoku...\n")

    solved, steps = solve(board)

    if solved:
        print("Solved!\n")
        for row in board:
            print(row)
    else:
        print("No solution found.")

    print(f"\nSteps: {steps}")
