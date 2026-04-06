"""
csp.py

Core CSP engine for Sudoku AI Solver.

Responsibilities:
- Manage board & domains
- Apply constraint propagation (AC-3)
- Execute backtracking search
- Provide clean API for external modules

Author: kennz_psix
"""

from typing import List, Set, Tuple, Optional
from copy import deepcopy

# Internal modules
from solver.ac3 import enforce_ac3
from solver.backtracking import backtrack, initialize_domains

Board = List[List[int]]
Domains = List[List[Set[int]]]


# ---------------------------------------------------------------------------
# CSP Model
# ---------------------------------------------------------------------------

class SudokuCSP:
    """
    Encapsulates Sudoku as a Constraint Satisfaction Problem.
    """

    def __init__(self, board: Board):
        self.board = deepcopy(board)
        self.domains = initialize_domains(self.board)
        self.steps = 0

    # -----------------------------------------------------------------------
    # Constraint Propagation
    # -----------------------------------------------------------------------

    def apply_ac3(self) -> None:
        """
        Apply AC-3 to reduce domains before search.
        """
        enforce_ac3(self.domains)

    # -----------------------------------------------------------------------
    # Solve
    # -----------------------------------------------------------------------

    def solve(self, use_ac3: bool = True) -> Tuple[bool, int]:
        """
        Solve Sudoku using CSP techniques.

        Args:
            use_ac3: apply AC-3 before backtracking

        Returns:
            (solved: bool, steps: int)
        """

        if use_ac3:
            try:
                self.apply_ac3()
            except ValueError:
                return False, self.steps

        steps_container = [0]

        success = backtrack(self.board, self.domains, steps_container)

        self.steps = steps_container[0]

        return success, self.steps

    # -----------------------------------------------------------------------
    # Utilities
    # -----------------------------------------------------------------------

    def is_solved(self) -> bool:
        """
        Check if board is fully assigned.
        """
        return all(
            self.board[r][c] != 0
            for r in range(9)
            for c in range(9)
        )

    def get_board(self) -> Board:
        """
        Return current board state.
        """
        return self.board

    def get_domains(self) -> Domains:
        """
        Return current domains.
        """
        return self.domains

    def reset(self, new_board: Board) -> None:
        """
        Reset CSP with a new board.
        """
        self.board = deepcopy(new_board)
        self.domains = initialize_domains(self.board)
        self.steps = 0


# ---------------------------------------------------------------------------
# High-Level API (Simple Interface)
# ---------------------------------------------------------------------------

def solve_sudoku(board: Board, use_ac3: bool = True) -> Tuple[bool, Board, int]:
    """
    High-level API for solving Sudoku.

    Args:
        board: input Sudoku
        use_ac3: enable AC-3 pre-processing

    Returns:
        (solved, solved_board, steps)
    """

    csp = SudokuCSP(board)

    success, steps = csp.solve(use_ac3=use_ac3)

    return success, csp.get_board(), steps


# ---------------------------------------------------------------------------
# Debug / Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
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

    print("Running CSP Sudoku Solver...\n")

    solved, result_board, steps = solve_sudoku(sample_board)

    if solved:
        print("Solved Sudoku:\n")
        for row in result_board:
            print(row)
    else:
        print("No solution found.")

    print(f"\nSteps: {steps}")
