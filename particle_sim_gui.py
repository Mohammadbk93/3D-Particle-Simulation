import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation


# --- Core simulation classes (same as before) ---
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

    def __str__(self):
        return f"({self.v[0]:.2f}, {self.v[1]:.2f}, {self.v[2]:.2f})"

class Force:
    def __init__(self, direction, magnitude):
        self.direction = direction
        self.magnitude = magnitude

    def get_acceleration(self):
        return self.direction * self.magnitude

class Point3D:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.initial_velocity = velocity
        self.trajectory = [self.position.v.copy()]
        self.forces = []

    def apply_random_properties(self, a1, a2, v0min, v0max, num_forces, amin, amax):
        friction = np.random.uniform(a1, a2)
        vx, vy, vz = np.random.uniform(v0min, v0max, 3)
        self.initial_velocity = Vector3D(vx, vy, vz)
        self.velocity = self.initial_velocity

        for _ in range(num_forces):
            direction = Vector3D(*np.random.uniform(-1, 1, 3))
            magnitude = np.random.uniform(amin, amax)
            self.forces.append(Force(direction, magnitude))

    def update_position(self):
        net_force = Vector3D(0, 0, 0)
        for f in self.forces:
            net_force += f.get_acceleration()
        self.velocity += net_force
        self.position += self.velocity
        self.trajectory.append(self.position.v.copy())

class Simulation:
    def __init__(self, L, N, M, a1, a2, amin, amax, vmin, vmax, v0min, v0max, T):
        self.points = []
        self.T = T
        for _ in range(N):
            pos = Vector3D(*np.random.uniform(-L/2, L/2, 3))
            vel = Vector3D(*np.random.uniform(v0min, v0max, 3))
            p = Point3D(pos, vel)
            p.apply_random_properties(a1, a2, v0min, v0max, M, amin, amax)
            self.points.append(p)

    def run(self):
        for _ in range(self.T):
            for p in self.points:
                p.update_position()


# --- PyQt5 GUI with matplotlib animation ---
class SimulationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Particle Simulation")
        self.setGeometry(100, 100, 800, 600)

        self.num_particles = 5
        self.sim = None
        self.trajectories = []
        self.T = 20

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Canvas for 3D animation
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)
        self.ax.set_zlim(-100, 100)
        self.ax.set_title("3D Particle Motion")

        # Controls
        control_layout = QHBoxLayout()

        self.slider_label = QLabel("Particles: 5")
        control_layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(5)
        self.slider.valueChanged.connect(self.update_slider_label)
        control_layout.addWidget(self.slider)

        self.button = QPushButton("Run Simulation")
        self.button.clicked.connect(self.run_simulation)
        control_layout.addWidget(self.button)

        layout.addLayout(control_layout)
        self.setLayout(layout)

    def update_slider_label(self):
        val = self.slider.value()
        self.slider_label.setText(f"Particles: {val}")
        self.num_particles = val

    def run_simulation(self):
        self.ax.clear()
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)
        self.ax.set_zlim(-100, 100)
        self.ax.set_title("3D Particle Motion")

        self.sim = Simulation(
            L=100.0, N=self.num_particles, M=3,
            a1=0.1, a2=0.5,
            amin=-1.0, amax=1.0,
            vmin=-2.0, vmax=2.0,
            v0min=-1.0, v0max=1.0,
            T=self.T
        )
        self.sim.run()
        self.trajectories = [np.array(p.trajectory) for p in self.sim.points]

        self.scatters = [
            self.ax.plot([], [], [], 'o')[0]
            for _ in range(self.num_particles)
        ]

        self.anim = FuncAnimation(
            self.fig, self.update_frame,
            frames=self.T, interval=400, blit=False
        )
        self.canvas.draw()

    def update_frame(self, frame):
        for i, scatter in enumerate(self.scatters):
            traj = self.trajectories[i]
            if frame < len(traj):
                x, y, z = traj[frame]
                scatter.set_data([x], [y])
                scatter.set_3d_properties([z])
        return self.scatters


# --- Run the app ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec_())
