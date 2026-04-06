"""
ac3.py

Implementation of AC-3 (Arc Consistency Algorithm #3) for Sudoku CSP.

AC-3 enforces arc consistency by iteratively removing inconsistent values
from variable domains.

Author: YourName
"""

from typing import List, Set, Tuple
from collections import deque

Board = List[List[int]]
Domains = List[List[Set[int]]]
Arc = Tuple[Tuple[int, int], Tuple[int, int]]  # ((r1,c1), (r2,c2))


# ---------------------------------------------------------------------------
# Utility: Get peers
# ---------------------------------------------------------------------------

def get_peers(row: int, col: int) -> Set[Tuple[int, int]]:
    """
    Return all peer cells of (row, col).
    """
    peers = set()

    # Row & Column
    for i in range(9):
        if i != col:
            peers.add((row, i))
        if i != row:
            peers.add((i, col))

    # Subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r, c) != (row, col):
                peers.add((r, c))

    return peers


# ---------------------------------------------------------------------------
# AC-3 Core
# ---------------------------------------------------------------------------

def ac3(domains: Domains) -> bool:
    """
    Enforce arc consistency on the Sudoku CSP.

    Args:
        domains: 9x9 grid of sets representing possible values

    Returns:
        True if arc consistency is achieved
        False if any domain becomes empty (failure)
    """

    queue = deque()

    # Initialize queue with all arcs
    for row in range(9):
        for col in range(9):
            for peer in get_peers(row, col):
                queue.append(((row, col), peer))

    # Process queue
    while queue:
        (xi, xj) = queue.popleft()

        if revise(domains, xi, xj):
            r, c = xi

            # If domain wiped out → failure
            if not domains[r][c]:
                return False

            # Add all neighbors back to queue
            for xk in get_peers(r, c):
                if xk != xj:
                    queue.append((xk, xi))

    return True


# ---------------------------------------------------------------------------
# Revise Function
# ---------------------------------------------------------------------------

def revise(domains: Domains, xi: Tuple[int, int], xj: Tuple[int, int]) -> bool:
    """
    Revise the domain of xi with respect to xj.

    Remove values from xi that are inconsistent with xj.

    Returns:
        True if domain was modified
    """

    revised = False
    r1, c1 = xi
    r2, c2 = xj

    to_remove = set()

    for x in domains[r1][c1]:
        # Constraint: xi != xj
        # If no possible y in domain[xj] satisfies x != y → remove x
        if all(x == y for y in domains[r2][c2]):
            to_remove.add(x)

    if to_remove:
        domains[r1][c1] -= to_remove
        revised = True

    return revised


# ---------------------------------------------------------------------------
# Integration Helper
# ---------------------------------------------------------------------------

def enforce_ac3(domains: Domains) -> Domains:
    """
    Apply AC-3 and return updated domains.

    Raises:
        ValueError if inconsistency is detected
    """
    success = ac3(domains)

    if not success:
        raise ValueError("AC-3 detected inconsistency (empty domain).")

    return domains


# ---------------------------------------------------------------------------
# Debug / Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example: initialize full domains (all values possible)
    domains = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]

    # Example constraint: cell (0,0) is fixed to 5
    domains[0][0] = {5}

    print("Before AC-3:")
    print(domains[0][1])

    enforce_ac3(domains)

    print("After AC-3:")
    print(domains[0][1])
