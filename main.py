import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QLabel, QLineEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import tempfile

# -------------------------------
# Calcul formel et résolution
# -------------------------------

class MathEngine:
    def __init__(self):
        self.x, self.y, self.z = sp.symbols('x y z')
    
    def simplify(self, expr_str):
        try:
            expr = sp.sympify(expr_str)
            return sp.simplify(expr)
        except Exception as e:
            return f"Erreur: {e}"
    
    def derivative(self, expr_str, var='x'):
        try:
            var_sym = sp.symbols(var)
            expr = sp.sympify(expr_str)
            return sp.diff(expr, var_sym)
        except Exception as e:
            return f"Erreur: {e}"
    
    def integrate(self, expr_str, var='x'):
        try:
            var_sym = sp.symbols(var)
            expr = sp.sympify(expr_str)
            return sp.integrate(expr, var_sym)
        except Exception as e:
            return f"Erreur: {e}"
    
    def solve_eq(self, eq_str, var='x'):
        try:
            var_sym = sp.symbols(var)
            eq = sp.Eq(sp.sympify(eq_str), 0)
            sols = sp.solve(eq, var_sym)
            return sols
        except Exception as e:
            return f"Erreur: {e}"
    
    def solve_system(self, eqs_str_list, vars_list):
        try:
            eqs = [sp.Eq(sp.sympify(eq), 0) for eq in eqs_str_list]
            vars_syms = sp.symbols(vars_list)
            sols = sp.solve(eqs, vars_syms, dict=True)
            return sols
        except Exception as e:
            return f"Erreur: {e}"

# -------------------------------
# Widget matplotlib 2D Graph
# -------------------------------

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.fig.tight_layout()

# -------------------------------
# Fenêtre principale
# -------------------------------

class GraphCalcX(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GraphCalcX - Calculatrice Graphique Python")
        self.setGeometry(100, 100, 1200, 800)
        self.engine = MathEngine()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Input expression
        expr_layout = QHBoxLayout()
        expr_label = QLabel("Expr. (f(x), eq, système...) :")
        self.expr_input = QLineEdit()
        expr_layout.addWidget(expr_label)
        expr_layout.addWidget(self.expr_input)
        
        # Variable input
        var_layout = QHBoxLayout()
        var_label = QLabel("Variable(s) (ex: x ou x,y):")
        self.var_input = QLineEdit("x")
        var_layout.addWidget(var_label)
        var_layout.addWidget(self.var_input)
        
        # Mode selection
        mode_layout = QHBoxLayout()
        self.mode_select = QComboBox()
        self.mode_select.addItems([
            "Simplifier", "Dériver", "Intégrer",
            "Résoudre équation", "Résoudre système",
            "Tracer 2D", "Tracer 3D", "Géométrie 2D simple"
        ])
        mode_layout.addWidget(QLabel("Mode :"))
        mode_layout.addWidget(self.mode_select)
        
        # Bouton Exécuter
        self.run_button = QPushButton("Exécuter")
        self.run_button.clicked.connect(self.on_run)
        
        # Résultat
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        
        # Graphique 2D matplotlib
        self.canvas2d = MplCanvas(width=6, height=4)
        
        # Ajouter widgets au layout principal
        layout.addLayout(expr_layout)
        layout.addLayout(var_layout)
        layout.addLayout(mode_layout)
        layout.addWidget(self.run_button)
        layout.addWidget(QLabel("Résultat / Graphique 2D :"))
        layout.addWidget(self.result_output)
        layout.addWidget(self.canvas2d)
        
        self.setLayout(layout)
    
    def on_run(self):
        mode = self.mode_select.currentText()
        expr = self.expr_input.text().strip()
        var_str = self.var_input.text().strip()
        
        if not expr:
            QMessageBox.warning(self, "Erreur", "L'expression est vide.")
            return
        
        # Clear old plot
        self.canvas2d.ax.clear()
        self.result_output.clear()
        
        if mode == "Simplifier":
            res = self.engine.simplify(expr)
            self.result_output.setText(str(res))
        
        elif mode == "Dériver":
            res = self.engine.derivative(expr, var=var_str)
            self.result_output.setText(str(res))
        
        elif mode == "Intégrer":
            res = self.engine.integrate(expr, var=var_str)
            self.result_output.setText(str(res))
        
        elif mode == "Résoudre équation":
            sols = self.engine.solve_eq(expr, var=var_str)
            self.result_output.setText(str(sols))
        
        elif mode == "Résoudre système":
            # expr must be a comma-separated list of eqs
            eqs = expr.split(",")
            vars_list = [v.strip() for v in var_str.split(",")]
            sols = self.engine.solve_system(eqs, vars_list)
            self.result_output.setText(str(sols))
        
        elif mode == "Tracer 2D":
            try:
                x = sp.symbols('x')
                f = sp.sympify(expr)
                f_lambd = sp.lambdify(x, f, modules=['numpy'])
                X = np.linspace(-10, 10, 500)
                Y = f_lambd(X)
                self.canvas2d.ax.plot(X, Y)
                self.canvas2d.ax.set_title(f"Graphique de y = {expr}")
                self.canvas2d.ax.grid(True)
                self.canvas2d.draw()
            except Exception as e:
                self.result_output.setText(f"Erreur de tracé 2D: {e}")
        
        elif mode == "Tracer 3D":
            # Tracé interactif 3D avec Plotly dans navigateur
            try:
                x, y = sp.symbols('x y')
                f = sp.sympify(expr)
                f_lambd = sp.lambdify((x, y), f, modules=['numpy'])
                X = np.linspace(-5, 5, 100)
                Y = np.linspace(-5, 5, 100)
                X, Y = np.meshgrid(X, Y)
                Z = f_lambd(X, Y)
                
                fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
                fig.update_layout(title=f"Surface 3D z = {expr}")
                # Affiche dans navigateur web par défaut
                tmp_html = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
                fig.write_html(tmp_html.name)
                webbrowser.open(f"file://{tmp_html.name}")
                self.result_output.setText("Graphique 3D affiché dans le navigateur.")
            except Exception as e:
                self.result_output.setText(f"Erreur de tracé 3D: {e}")
        
        elif mode == "Géométrie 2D simple":
            # Exemple : construction interactive d'un triangle, calcul angles/longueurs
            try:
                self.canvas2d.ax.clear()
                pts = np.array([[0,0],[3,0],[2,4]])
                tri = plt.Polygon(pts, fill=None, edgecolor='b')
                self.canvas2d.ax.add_patch(tri)
                self.canvas2d.ax.scatter(pts[:,0], pts[:,1], color='r')
                
                # Calculs
                def dist(a,b): return np.linalg.norm(a-b)
                dists = [dist(pts[i], pts[(i+1)%3]) for i in range(3)]
                a, b, c = dists
                # Angles via loi des cosinus
                A = np.degrees(np.arccos((b**2 + c**2 - a**2)/(2*b*c)))
                B = np.degrees(np.arccos((a**2 + c**2 - b**2)/(2*a*c)))
                C = 180 - A - B
                
                self.result_output.setText(
                    f"Longueurs des côtés: {a:.2f}, {b:.2f}, {c:.2f}\n"
                    f"Angles (en degrés): A={A:.2f}, B={B:.2f}, C={C:.2f}"
                )
                self.canvas2d.ax.set_xlim(-1,5)
                self.canvas2d.ax.set_ylim(-1,5)
                self.canvas2d.ax.set_aspect('equal', 'box')
                self.canvas2d.ax.grid(True)
                self.canvas2d.draw()
            except Exception as e:
                self.result_output.setText(f"Erreur géométrie 2D: {e}")
        
        else:
            self.result_output.setText("Mode non implémenté.")
    

def main():
    app = QApplication(sys.argv)
    window = GraphCalcX()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
