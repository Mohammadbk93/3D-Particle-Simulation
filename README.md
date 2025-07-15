# 3D Particle Simulation and Visualization

This project showcases a modular system for generating, visualizing, and fetching 3D particle data using Python. It integrates RESTful APIs, interactive 3D visualization with PyVista, GUI development with Tkinter, and data fetching from external web services. The project is designed with real-world applications in mind, such as simulation, scientific visualization, and API integration.

## Features

- FastAPI backend serving random 3D particle data
- Tkinter GUI to display fetched particle data
- 3D visualization using PyVista
- External API integration (REST) to simulate real-world data fetching
- Conversion to standalone `.exe` files using PyInstaller

---

## 🎯 Project Objectives (Implemented in Python)

---

### • Use Qt to create a GUI for visualization  
> **Adapted in Python using Tkinter**  
I implemented a lightweight GUI for simulation control and launch using **Tkinter**, a native Python GUI library. While not Qt, it serves the same purpose: launching and interacting with the simulation without using the command line.  
📄 File: `particle_sim_gui.py`
![python_4LeENpByzs](https://github.com/user-attachments/assets/125f0bf0-c4c3-43c9-bca5-6709c47a2410)

---

### • Use VTK to render the 3D scene  
> **Achieved using PyVista (VTK-based)**  
For real-time 3D rendering and animation of particles, I used **PyVista**, a Python wrapper around the Visualization Toolkit (VTK). It enables interactive 3D plotting and is fully compatible with scientific visualization workflows.  
📄 File: `particle_sim_pyvista.py`
![devWifz](https://github.com/user-attachments/assets/f00f8ab6-46e6-46d0-9607-829eb1299c29)

---

### • Fetch initial data from a web server  
> **Accomplished via FastAPI & External API Integration**  
I used two approaches:
- Built a **local REST API server** using **FastAPI** to generate and serve random particle data.  
  📄 File: `particle_api_server.py`
- Integrated with an **external public API** (`https://jsonplaceholder.typicode.com/users`) to simulate particles from real data.  
  📄 File: `task_fetch_from_api.py`
![particle_simulator_aybLKU6Oaj](https://github.com/user-attachments/assets/386dfd81-738a-48ee-9605-6a79d4a01ffd)

---

### • Build a distributable installation package  
> **Implemented via PyInstaller**  
I used **PyInstaller** to convert Python scripts into standalone `.exe` executables for Windows. These packages include all necessary dependencies, making them portable and easy to run on any machine without requiring Python installation.  
📦 Output Folder: `/dist/`  
📄 Config Files: `*.spec`
<img width="519" height="47" alt="3D_par_sim_2" src="https://github.com/user-attachments/assets/51194046-b51e-4723-bdc7-5d3249239bc8" />

---
## 📦 Package Dependencies

Before running the project, make sure to install the following Python packages. You can use `pip` to install them manually, or use the provided virtual environment or `requirements.txt` if available.

### Required Packages

| Package         | Purpose                                              |
|----------------|------------------------------------------------------|
| `fastapi`       | For building the REST API server                    |
| `uvicorn`       | ASGI server to run FastAPI                          |
| `requests`      | To fetch data from external APIs                    |
| `pyvista`       | VTK-based 3D visualization                          |
| `vtk`           | Backend engine for PyVista                          |
| `tkinter`       | GUI creation (comes pre-installed with Python)     |
| `pyinstaller`   | To package Python scripts into `.exe` executables   |







