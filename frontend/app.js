/**
 * app.js
 *
 * Frontend controller for Sudoku AI Solver Web App.
 *
 * Features:
 * - Dynamic grid rendering
 * - User input handling
 * - API integration (solve)
 * - Basic visualization hooks
 *
 * Author: kennz_psix
 */

const SIZE = 9;
let board = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));


// ---------------------------------------------------------------------------
// Grid Rendering
// ---------------------------------------------------------------------------

function createGrid() {
    const grid = document.getElementById("sudoku-grid");
    grid.innerHTML = "";

    for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
            const cell = document.createElement("input");
            cell.type = "text";
            cell.maxLength = 1;
            cell.classList.add("cell");

            // Styling blocks
            if ((r + 1) % 3 === 0) cell.style.borderBottom = "2px solid black";
            if ((c + 1) % 3 === 0) cell.style.borderRight = "2px solid black";

            cell.dataset.row = r;
            cell.dataset.col = c;

            cell.addEventListener("input", handleInput);

            grid.appendChild(cell);
        }
    }
}


// ---------------------------------------------------------------------------
// Input Handling
// ---------------------------------------------------------------------------

function handleInput(e) {
    const val = e.target.value;
    const r = parseInt(e.target.dataset.row);
    const c = parseInt(e.target.dataset.col);

    if (!/^[1-9]$/.test(val)) {
        e.target.value = "";
        board[r][c] = 0;
        return;
    }

    board[r][c] = parseInt(val);
}


// ---------------------------------------------------------------------------
// Update UI from Board
// ---------------------------------------------------------------------------

function updateGrid(newBoard) {
    const cells = document.querySelectorAll(".cell");

    cells.forEach(cell => {
        const r = parseInt(cell.dataset.row);
        const c = parseInt(cell.dataset.col);

        cell.value = newBoard[r][c] === 0 ? "" : newBoard[r][c];
    });
}


// ---------------------------------------------------------------------------
// Solve API Call
// ---------------------------------------------------------------------------

async function solveSudoku(algorithm = "csp") {
    try {
        setStatus("Solving...");

        const response = await fetch("/solve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                board: board,
                algorithm: algorithm
            })
        });

        const data = await response.json();

        if (data.success) {
            board = data.board;
            updateGrid(board);
            setStatus(`Solved in ${data.steps} steps`);
        } else {
            setStatus("No solution found");
        }

    } catch (err) {
        console.error(err);
        setStatus("Error solving Sudoku");
    }
}


// ---------------------------------------------------------------------------
// Controls
// ---------------------------------------------------------------------------

function clearBoard() {
    board = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));
    updateGrid(board);
    setStatus("Board cleared");
}

function loadExample() {
    board = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ];

    updateGrid(board);
    setStatus("Example loaded");
}


// ---------------------------------------------------------------------------
// Status UI
// ---------------------------------------------------------------------------

function setStatus(message) {
    const el = document.getElementById("status");
    el.textContent = message;
}


// ---------------------------------------------------------------------------
// Visualization Hook (optional upgrade)
// ---------------------------------------------------------------------------

function highlightCell(row, col) {
    const cells = document.querySelectorAll(".cell");

    cells.forEach(cell => {
        cell.classList.remove("highlight");
    });

    const target = document.querySelector(
        `.cell[data-row='${row}'][data-col='${col}']`
    );

    if (target) {
        target.classList.add("highlight");
    }
}


// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    createGrid();

    document.getElementById("solve-btn")
        .addEventListener("click", () => solveSudoku("csp"));

    document.getElementById("dlx-btn")
        .addEventListener("click", () => solveSudoku("dlx"));

    document.getElementById("clear-btn")
        .addEventListener("click", clearBoard);

    document.getElementById("example-btn")
        .addEventListener("click", loadExample);
});
