import sys
import requests
import numpy as np
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
import pyvista as pv
from pyvistaqt import QtInteractor

class ParticleSimApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("API Particle Simulation")
        self.setMinimumWidth(300)

        self.layout = QVBoxLayout()
        self.label = QLabel("Click to fetch user data and run simulation:")
        self.button = QPushButton("Start Simulation")
        self.button.clicked.connect(self.run_simulation)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def run_simulation(self):
        # Step 1: Fetch from public API
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=5)
            data = response.json()
            users = [user["name"] for user in data]
        except Exception as e:
            self.label.setText(f"Failed to fetch data: {e}")
            return

        if not users:
            self.label.setText("No user data found.")
            return

        self.label.setText(f"Fetched {len(users)} users. Running simulation...")

        # Step 2: Visualize with pyvista
        plotter = pv.Plotter(window_size=[800, 600])
        spheres = []

        for name in users:
            pos = np.random.uniform(-50, 50, size=3)
            sphere = pv.Sphere(radius=2.0, center=pos)
            actor = plotter.add_mesh(sphere, color=np.random.choice(['red', 'green', 'blue', 'yellow']))
            plotter.add_point_labels([pos], [name], font_size=10, point_color='white', text_color='white')
            spheres.append((sphere, actor, pos))

        plotter.show(title="Simulated User Particles")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParticleSimApp()
    window.show()
    sys.exit(app.exec_())
