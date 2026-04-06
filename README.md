<div align="center">

<h1>🧩 Sudoku AI Solver Pro</h1>

<p>
⚡ Advanced Constraint Solving • 🚀 Visualization • 🤖 AI-Powered Logic
</p>

<p>
<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi">
<img src="https://img.shields.io/badge/AI-CSP%20Solver-purple?style=for-the-badge">
<img src="https://img.shields.io/badge/UI-Interactive-orange?style=for-the-badge">
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>

</div>

---

## 🌟 Overview

<b>Sudoku AI Solver Pro</b> is an advanced system for solving Sudoku using modern AI and constraint-based techniques.

It combines:

<ul>
<li>🧠 Constraint Satisfaction Problem (CSP)</li>
<li>⚡ Heuristic Search (MRV, Degree, LCV)</li>
<li>🔗 Arc Consistency (AC-3)</li>
<li>💀 Dancing Links (Algorithm X)</li>
</ul>

<p><i>More than a solver — a full algorithm visualization system.</i></p>

---

## 🚀 Features

### 🔥 Core Engine

<ul>
<li>Backtracking Solver</li>
<li>CSP Solver (MRV + Degree + LCV)</li>
<li>AC-3 Constraint Propagation</li>
<li>DLX (Ultra-fast exact cover solver)</li>
</ul>

### 🎨 Interactive UI

<ul>
<li>Dynamic Sudoku grid</li>
<li>Real-time solving</li>
<li>Step highlighting</li>
</ul>

### 📊 Performance Analysis

<ul>
<li>Execution time</li>
<li>Steps / Backtracks</li>
<li>Algorithm comparison (CSP vs DLX)</li>
</ul>

---

## 🧠 Algorithms

<table align="center">
<tr>
<th>Level</th>
<th>Technique</th>
</tr>
<tr>
<td>Basic</td>
<td>Backtracking</td>
</tr>
<tr>
<td>Intermediate</td>
<td>MRV + Forward Checking</td>
</tr>
<tr>
<td>Advanced</td>
<td>CSP + AC-3</td>
</tr>
<tr>
<td>💀 Expert</td>
<td>Dancing Links (DLX)</td>
</tr>
</table>

---

## 📸 Demo

<p align="center">
<img src="https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif" width="500"/>
</p>

<p align="center"><i>Visualization demo (placeholder)</i></p>

---

## ⚙️ Installation

```bash
git clone https://github.com/ManucianTeam/sudoku-ai-solver-pro.git
cd sudoku-ai-solver-pro

pip install -r requirements.txt
```

---

## ▶️ Run Backend

```bash
uvicorn server:app --reload
```

<p>
Open:
<br>
<code>http://127.0.0.1:8000/docs</code>
</p>

---

## 🌐 Run Frontend

<p>
Open file:
<br>
<code>web/index.html</code>
</p>

---

## 🔌 API Example

<b>POST /solve</b>

```json
{
  "board": [[...]],
  "algorithm": "csp"
}
```

<b>Response:</b>

```json
{
  "success": true,
  "board": [[...]],
  "steps": 123
}
```

---

## 🏗️ Project Structure

```bash
sudoku-ai-solver-pro/
│
├── solver/
├── heuristics/
├── utils/
├── web/
│
├── server.py
├── pyproject.toml
├── README.md
```

---

## 🧪 Testing

```bash
pytest
```

---

## 🧠 Architecture

```text
Frontend (JavaScript)
        ↓
FastAPI Backend
        ↓
CSP / DLX Engine
```

---

## ⚡ Performance Insight

<ul>
<li>CSP → flexible, explainable</li>
<li>DLX → extremely fast (exact cover)</li>
</ul>

<p><i>Hybrid approach = speed + intelligence</i></p>

---

## 🔮 Future Improvements

<ul>
<li>WebSocket real-time solving</li>
<li>Benchmark dashboard</li>
<li>AI explanation system</li>
<li>Mobile UI</li>
</ul>

---

## 📄 License

MIT License

---

## ⭐ Contributing

Pull requests are welcome.
For major changes, open an issue first.

---

## 💡 Final Note

This project demonstrates:

<ul>
<li>Algorithmic thinking</li>
<li>AI problem solving</li>
<li>Full-stack integration</li>
</ul>

<p align="center"><b>🚀 Built as a portfolio-grade system</b></p>
