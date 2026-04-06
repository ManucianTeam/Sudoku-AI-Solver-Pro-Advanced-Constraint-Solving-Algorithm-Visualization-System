"""
degree.py

Advanced implementation of the Degree Heuristic for Sudoku CSP solvers.

This module provides:
- Efficient degree computation
- Integration with MRV (Minimum Remaining Values)
- Clean, extensible design for production-level solvers

Author: YourName
"""

from typing import List, Tuple, Set

Board = List[List[int]]


# ---------------------------------------------------------------------------
# Utility: Get peers of a cell (row, col)
# ---------------------------------------------------------------------------

def get_peers(row: int, col: int) -> Set[Tuple[int, int]]:
    """
    Return all peer coordinates of a given cell in Sudoku.

    Peers include:
    - Same row
    - Same column
    - Same 3x3 subgrid

    Returns:
        A set of (row, col) tuples representing peer cells.
    """
    peers = set()

    # Row & Column peers
    for i in range(9):
        if i != col:
            peers.add((row, i))
        if i != row:
            peers.add((i, col))

    # Subgrid peers
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r, c) != (row, col):
                peers.add((r, c))

    return peers


# ---------------------------------------------------------------------------
# Degree Heuristic
# ---------------------------------------------------------------------------

def compute_degree(board: Board, row: int, col: int) -> int:
    """
    Compute the degree of a variable (cell).

    Degree = number of unassigned neighboring variables (peers).

    Args:
        board: 9x9 Sudoku board
        row, col: cell position

    Returns:
        Integer degree value
    """
    peers = get_peers(row, col)

    # Count how many peers are still unassigned (value == 0)
    return sum(1 for r, c in peers if board[r][c] == 0)


# ---------------------------------------------------------------------------
# Combined MRV + Degree Heuristic (tie-breaker)
# ---------------------------------------------------------------------------

def select_variable_with_degree(
    board: Board,
    domains: List[List[Set[int]]]
) -> Tuple[int, int]:
    """
    Select the next variable using:
    1. MRV (Minimum Remaining Values)
    2. Degree Heuristic (tie-breaker)

    Strategy:
    - First, pick cells with the smallest domain size (MRV)
    - If multiple candidates exist, pick the one with the highest degree

    Args:
        board: Sudoku board
        domains: 9x9 structure containing possible values for each cell

    Returns:
        (row, col) of selected variable
    """

    candidates = []

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                domain_size = len(domains[row][col])

                # Skip invalid states (empty domain)
                if domain_size == 0:
                    continue

                degree = compute_degree(board, row, col)

                # Sort key:
                # - smaller domain first (MRV)
                # - higher degree first → use negative
                candidates.append((domain_size, -degree, row, col))

    if not candidates:
        raise ValueError("No valid unassigned variables found.")

    # Sort by MRV, then Degree
    candidates.sort()

    _, _, row, col = candidates[0]
    return row, col


# ---------------------------------------------------------------------------
# Optional Optimization: Cached Degree (for performance)
# ---------------------------------------------------------------------------

class DegreeCache:
    """
    Optional caching layer to avoid recomputing degrees repeatedly.

    Useful for large-scale or repeated solving scenarios.
    """

    def __init__(self):
        self.cache = {}

    def get(self, board: Board, row: int, col: int) -> int:
        key = (row, col)

        # NOTE:
        # This simple cache assumes board changes invalidate relevance.
        # For production, consider hashing board state.
        if key not in self.cache:
            self.cache[key] = compute_degree(board, row, col)

        return self.cache[key]

    def clear(self):
        """Clear cache when board state changes significantly."""
        self.cache.clear()


# ---------------------------------------------------------------------------
# Debug / Example Usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example board (0 = empty)
    sample_board = [
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

    # Dummy domains (for demo only)
    domains = [[set(range(1, 10)) if cell == 0 else {cell}
                for cell in row] for row in sample_board]

    r, c = select_variable_with_degree(sample_board, domains)
    print(f"Selected cell: ({r}, {c}) with degree = {compute_degree(sample_board, r, c)}")
