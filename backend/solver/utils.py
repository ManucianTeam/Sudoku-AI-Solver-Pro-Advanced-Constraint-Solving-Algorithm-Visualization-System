"""
utils.py

Utility functions for Sudoku AI Solver.

Features:
- Board validation
- Pretty printing
- Sudoku generator (basic)
- Deep copy helpers
- State checks

Author: kennz_psix
"""

from typing import List, Tuple
import random
import copy

Board = List[List[int]]


# ---------------------------------------------------------------------------
# Pretty Print
# ---------------------------------------------------------------------------

def print_board(board: Board) -> None:
    """
    Pretty-print Sudoku board with grid formatting.
    """
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            val = board[i][j]
            print(val if val != 0 else ".", end=" ")

        print()
    print()


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def is_valid_board(board: Board) -> bool:
    """
    Check if the board is valid (no duplicates in row/col/box).
    """

    def is_valid_group(nums):
        nums = [n for n in nums if n != 0]
        return len(nums) == len(set(nums))

    # Rows & Columns
    for i in range(9):
        if not is_valid_group(board[i]):
            return False
        if not is_valid_group([board[r][i] for r in range(9)]):
            return False

    # Subgrids
    for box_row in range(3):
        for box_col in range(3):
            nums = []
            for r in range(3):
                for c in range(3):
                    nums.append(board[box_row*3 + r][box_col*3 + c])
            if not is_valid_group(nums):
                return False

    return True


def is_complete(board: Board) -> bool:
    """
    Check if Sudoku is completely filled.
    """
    return all(board[r][c] != 0 for r in range(9) for c in range(9))


# ---------------------------------------------------------------------------
# Board Utilities
# ---------------------------------------------------------------------------

def copy_board(board: Board) -> Board:
    """
    Deep copy board safely.
    """
    return copy.deepcopy(board)


def find_empty(board: Board) -> Tuple[int, int] or None:
    """
    Find first empty cell.
    """
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


# ---------------------------------------------------------------------------
# Sudoku Generator (basic)
# ---------------------------------------------------------------------------

def generate_full_board() -> Board:
    """
    Generate a full valid Sudoku board using backtracking.
    """

    board = [[0]*9 for _ in range(9)]

    def is_valid(r, c, val):
        if any(board[r][i] == val for i in range(9)):
            return False
        if any(board[i][c] == val for i in range(9)):
            return False

        sr, sc = 3*(r//3), 3*(c//3)
        for i in range(3):
            for j in range(3):
                if board[sr+i][sc+j] == val:
                    return False
        return True

    def fill():
        empty = find_empty(board)
        if not empty:
            return True

        r, c = empty
        nums = list(range(1, 10))
        random.shuffle(nums)

        for val in nums:
            if is_valid(r, c, val):
                board[r][c] = val
                if fill():
                    return True
                board[r][c] = 0

        return False

    fill()
    return board


def remove_numbers(board: Board, difficulty: str = "medium") -> Board:
    """
    Remove numbers from a full board to create a puzzle.

    difficulty:
        easy   -> fewer removals
        medium -> moderate
        hard   -> many removals
    """

    board = copy_board(board)

    levels = {
        "easy": 30,
        "medium": 40,
        "hard": 50
    }

    removals = levels.get(difficulty, 40)

    while removals > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)

        if board[r][c] != 0:
            board[r][c] = 0
            removals -= 1

    return board


def generate_sudoku(difficulty: str = "medium") -> Board:
    """
    Generate a playable Sudoku puzzle.
    """
    full = generate_full_board()
    return remove_numbers(full, difficulty)


# ---------------------------------------------------------------------------
# Benchmark Utility
# ---------------------------------------------------------------------------

def measure_time(func, *args, **kwargs):
    """
    Measure execution time of a function.
    """
    import time

    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()

    return result, end - start


# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating Sudoku...\n")

    puzzle = generate_sudoku("medium")
    print_board(puzzle)

    print("Valid:", is_valid_board(puzzle))
