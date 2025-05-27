raphCalcX is a feature-rich symbolic and graphical calculator built entirely in Python. Whether you're a high school student, university researcher, or a curious learner, GraphCalcX is your all-in-one companion for solving equations, plotting functions, and exploring advanced mathematical concepts — no AI query required.
⚙️ Features
🧠 Symbolic Computation (Powered by SymPy)

    Solve linear, polynomial, and transcendental equations.

    Symbolic differentiation and integration.

    Taylor expansions, limits, simplification, factorization.

    Recurrence relations and root finding using Newton’s method.

📊 Graphing Capabilities (With Matplotlib)

    Plot 2D functions: cartesian, polar, and parametric.

    Customize axes, labels, legends, and domains.

    Animate functions and parameter changes.

🔢 Numerical Tools (Via NumPy)

    Numerical solvers and optimizers.

    Evaluate expressions over intervals or datasets.

    Root approximation and iteration-based methods.

🎓 Educational Mode

    Step-by-step output for differentiation, solving, and integration.

    Built-in examples and learning-oriented explanations.

    Lightweight interface mode for beginners.

💡 Why Use GraphCalcX?

    Offline & Open Source: No need for internet or AI services.

    Extensible: Modular Python structure — easy to plug in your own methods.

    Cross-platform: Works on Windows, Linux, macOS (with Python ≥ 3.8).

    Minimalist Interface: Fast, intuitive CLI and optional GUI coming soon.

🚀 Quick Start

# 1. Clone the repository
git clone https://github.com/yourname/graphcalcx-python.git
cd graphcalcx-python

# 2. Create virtual environment and activate it
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the CLI calculator
python main.py

🗂️ Project Structure

graphcalcx-python/
├── core/              # Symbolic and numeric engine
│   ├── solver.py
│   ├── calculus.py
│   └── plotter.py
├── examples/          # Example scripts and use cases
├── main.py            # CLI entry point
├── tests/             # Unit tests
├── requirements.txt
└── README.md

🧪 Coming Soon

    GUI version with PyQt5 / tkinter.

    Interactive geometry and 3D plots.

    Export to LaTeX and PNG.

    Plugin system for user-defined functions.

📜 License

MIT License — free to use, modify, and distribute.
