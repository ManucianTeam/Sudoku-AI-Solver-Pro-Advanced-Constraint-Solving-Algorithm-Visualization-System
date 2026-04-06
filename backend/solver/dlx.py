"""
dlx.py

Implementation of Algorithm X with Dancing Links (DLX)
for solving exact cover problems (e.g., Sudoku).

Based on Donald Knuth's paper:
"Dancing Links" (2000)

Author: kennz_psix
"""

from typing import Optional, List


# ---------------------------------------------------------------------------
# Dancing Links Node
# ---------------------------------------------------------------------------

class Node:
    def __init__(self):
        self.left: 'Node' = self
        self.right: 'Node' = self
        self.up: 'Node' = self
        self.down: 'Node' = self
        self.column: 'ColumnNode' = None


class ColumnNode(Node):
    def __init__(self, name: str):
        super().__init__()
        self.size = 0
        self.name = name


# ---------------------------------------------------------------------------
# DLX Structure
# ---------------------------------------------------------------------------

class DLX:
    def __init__(self, matrix: List[List[int]]):
        self.header = ColumnNode("header")
        self.columns: List[ColumnNode] = []
        self.solution: List[Node] = []

        self._build(matrix)

    # -----------------------------------------------------------------------
    # Build structure
    # -----------------------------------------------------------------------

    def _build(self, matrix: List[List[int]]):

        num_cols = len(matrix[0])

        # Create column headers
        for i in range(num_cols):
            col = ColumnNode(str(i))
            self.columns.append(col)

            col.right = self.header
            col.left = self.header.left
            self.header.left.right = col
            self.header.left = col

        # Create rows
        for row in matrix:
            prev = None

            for j, val in enumerate(row):
                if val == 1:
                    col = self.columns[j]
                    node = Node()
                    node.column = col

                    # Vertical linking
                    node.down = col
                    node.up = col.up
                    col.up.down = node
                    col.up = node

                    col.size += 1

                    # Horizontal linking
                    if prev is None:
                        prev = node
                        node.right = node
                        node.left = node
                    else:
                        node.right = prev
                        node.left = prev.left
                        prev.left.right = node
                        prev.left = node

    # -----------------------------------------------------------------------
    # Cover / Uncover
    # -----------------------------------------------------------------------

    def cover(self, col: ColumnNode):
        col.right.left = col.left
        col.left.right = col.right

        i = col.down
        while i != col:
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1
                j = j.right
            i = i.down

    def uncover(self, col: ColumnNode):
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.column.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up

        col.right.left = col
        col.left.right = col

    # -----------------------------------------------------------------------
    # Algorithm X
    # -----------------------------------------------------------------------

    def search(self, k: int = 0) -> bool:
        """
        Recursive search for exact cover solution.
        """

        if self.header.right == self.header:
            return True  # solved

        # Choose column with smallest size (heuristic)
        col = self._choose_column()

        self.cover(col)

        r = col.down
        while r != col:
            self.solution.append(r)

            j = r.right
            while j != r:
                self.cover(j.column)
                j = j.right

            if self.search(k + 1):
                return True

            # Backtrack
            self.solution.pop()

            j = r.left
            while j != r:
                self.uncover(j.column)
                j = j.left

            r = r.down

        self.uncover(col)
        return False

    def _choose_column(self) -> ColumnNode:
        """
        Heuristic: choose column with minimum size.
        """
        min_col = None
        min_size = float("inf")

        c = self.header.right
        while c != self.header:
            if c.size < min_size:
                min_size = c.size
                min_col = c
            c = c.right

        return min_col


# ---------------------------------------------------------------------------
# Sudoku → Exact Cover Conversion
# ---------------------------------------------------------------------------

def sudoku_to_exact_cover(board: List[List[int]]) -> List[List[int]]:
    """
    Convert Sudoku to exact cover matrix.
    """

    def index(r, c, v):
        return r * 81 + c * 9 + v

    matrix = []

    for r in range(9):
        for c in range(9):
            for v in range(1, 10):

                if board[r][c] != 0 and board[r][c] != v:
                    continue

                row = [0] * 324

                # Cell constraint
                row[r * 9 + c] = 1

                # Row constraint
                row[81 + r * 9 + (v - 1)] = 1

                # Column constraint
                row[162 + c * 9 + (v - 1)] = 1

                # Box constraint
                box = (r // 3) * 3 + (c // 3)
                row[243 + box * 9 + (v - 1)] = 1

                matrix.append(row)

    return matrix


# ---------------------------------------------------------------------------
# Solve Sudoku using DLX
# ---------------------------------------------------------------------------

def solve_sudoku_dlx(board: List[List[int]]) -> List[List[int]]:
    """
    Solve Sudoku using DLX.
    """

    matrix = sudoku_to_exact_cover(board)
    dlx = DLX(matrix)

    if not dlx.search():
        raise ValueError("No solution found.")

    # NOTE:
    # Mapping back solution rows → Sudoku grid is simplified here
    # For full implementation, track (r,c,v) mapping explicitly

    return board  # placeholder (extend for full mapping)


# ---------------------------------------------------------------------------
# Debug
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

    print("Solving with DLX...\n")

    try:
        solve_sudoku_dlx(board)
        print("Solved (structure built successfully)")
    except ValueError:
        print("No solution found.")
