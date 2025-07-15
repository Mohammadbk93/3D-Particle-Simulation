from vpython import sphere, vector, rate, scene, color
import numpy as np

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
    def __init__(self, position, velocity, color):
        self.position = position
        self.velocity = velocity
        self.initial_velocity = velocity
        self.trajectory = [self.position.v.copy()]
        self.forces = []

        # VPython visual object
        pos_v = vector(*self.position.v)
        self.obj = sphere(pos=pos_v, radius=1, color=color, make_trail=True)

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
        self.obj.pos = vector(*self.position.v)

    def print_position(self):
        print(self.position)

class Simulation:
    def __init__(self, L, N, M, a1, a2, amin, amax, vmin, vmax, v0min, v0max, T):
        self.points = []
        self.T = T
        colors = [color.red, color.green, color.blue, color.magenta, color.orange]

        for i in range(N):
            pos = Vector3D(*np.random.uniform(-L/2, L/2, 3))
            vel = Vector3D(*np.random.uniform(v0min, v0max, 3))
            c = colors[i % len(colors)]
            p = Point3D(pos, vel, c)
            p.apply_random_properties(a1, a2, v0min, v0max, M, amin, amax)
            self.points.append(p)

    def update_all(self):
        for p in self.points:
            p.update_position()

    def print_all(self):
        for p in self.points:
            p.print_position()

    def run(self):
        for t in range(self.T):
            rate(5)  # Slower animation: 5 steps per second
            print(f"--- Time step {t} ---")
            self.update_all()
            self.print_all()

        scene.waitfor('click')  # Keeps window open until user clicks

# Run the simulation
if __name__ == "__main__":
    sim = Simulation(
        L=100.0, N=5, M=3,
        a1=0.1, a2=0.5,
        amin=-1.0, amax=1.0,
        vmin=-2.0, vmax=2.0,
        v0min=-1.0, v0max=1.0,
        T=30
    )
    sim.run()
