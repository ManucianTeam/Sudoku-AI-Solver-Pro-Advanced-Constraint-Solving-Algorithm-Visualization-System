"""
server.py

FastAPI backend for Sudoku AI Solver.
Supports CSP + DLX solving.

Run:
    uvicorn server:app --reload

Author: kennz_psix
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os

# Import solver
from solver.csp import solve_sudoku
from solver.dlx import solve_sudoku_dlx

# ---------------------------------------------------------------------------
# Config (from .env)
# ---------------------------------------------------------------------------

PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
DEFAULT_ALGO = os.getenv("DEFAULT_ALGORITHM", "csp")

# ---------------------------------------------------------------------------
# App Init
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Sudoku AI Solver API",
    description="CSP + DLX Solver Backend",
    version="1.0.0"
)


# ---------------------------------------------------------------------------
# Request Model
# ---------------------------------------------------------------------------

class SolveRequest(BaseModel):
    board: List[List[int]]
    algorithm: str = DEFAULT_ALGO


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Sudoku AI Solver API is running"}


@app.post("/solve")
def solve(req: SolveRequest):
    board = req.board
    algo = req.algorithm.lower()

    if len(board) != 9 or any(len(row) != 9 for row in board):
        raise HTTPException(status_code=400, detail="Invalid board size")

    try:
        if algo == "dlx":
            solved_board = solve_sudoku_dlx(board)
            return {
                "success": True,
                "board": solved_board,
                "steps": 0
            }

        elif algo == "csp":
            success, solved_board, steps = solve_sudoku(board)
            return {
                "success": success,
                "board": solved_board,
                "steps": steps
            }

        else:
            raise HTTPException(status_code=400, detail="Unknown algorithm")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Run (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=DEBUG)
