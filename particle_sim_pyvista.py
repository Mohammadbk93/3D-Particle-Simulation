import sys
import time
import numpy as np
import pyvista as pv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QSlider
)
from PyQt5.QtCore import Qt

# --- Core simulation classes ---
class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.v = np.array([x, y, z], dtype=float)

    def __add__(self, other):
        return Vector3D(*(self.v + other.v))

    def __iadd__(self, other):
        self.v += other.v
        return self

    def __mul__(self, scalar):
        return Vector3D(*(self.v * scalar))


class Force:
    def __init__(self, direction, magnitude):
        self.direction = direction
        self.magnitude = magnitude


class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector3D()

    def apply_force(self, force):
        acceleration = force.direction * force.magnitude
        self.velocity += acceleration

    def move(self):
        self.position += self.velocity


class Simulation:
    def __init__(self, num_particles):
        self.particles = [
            Particle(Vector3D(
                np.random.uniform(-50, 50),
                np.random.uniform(-50, 50),
                np.random.uniform(20, 70)
            )) for _ in range(num_particles)
        ]
        self.gravity = Force(Vector3D(0, 0, -1), 0.1)
        self.T = 100

    def step(self):
        for p in self.particles:
            p.apply_force(self.gravity)
            p.move()


# --- PyQt5 GUI ---
class ParticleSimApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Particle Simulator (PyQt + PyVista)")
        self.setGeometry(100, 100, 320, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel("Select number of particles:")
        self.layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(10)
        self.slider.valueChanged.connect(self.update_slider_label)
        self.layout.addWidget(self.slider)

        self.slider_value_label = QLabel("Particles: 10")
        self.layout.addWidget(self.slider_value_label)

        self.button = QPushButton("Start Simulation")
        self.button.clicked.connect(self.run_simulation)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def update_slider_label(self):
        self.slider_value_label.setText(f"Particles: {self.slider.value()}")

    def run_simulation(self):
        n_particles = self.slider.value()
        sim = Simulation(n_particles)

        plotter = pv.Plotter()
        plotter.set_background("black")
        plotter.add_axes()
        spheres = []

        for p in sim.particles:
            sphere = pv.Sphere(radius=2.0, center=p.position.v)
            actor = plotter.add_mesh(sphere, color=np.random.choice(['red', 'green', 'blue', 'yellow', 'cyan']))
            spheres.append((sphere, actor, p))

        for t in range(sim.T):
            sim.step()
            for i, (sphere, actor, p) in enumerate(spheres):
                new_sphere = pv.Sphere(radius=2.0, center=p.position.v)
                actor.mapper.SetInputData(new_sphere)
            plotter.render()
            time.sleep(0.05)

        plotter.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ParticleSimApp()
    window.show()
    sys.exit(app.exec_())
