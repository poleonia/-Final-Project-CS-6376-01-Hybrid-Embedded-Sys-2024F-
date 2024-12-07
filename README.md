# Aircraft Collision Avoidance System (ACAS) in 3D Environments

![Simulation](https://your-image-link-here) <!-- Optional: Include a visual representation -->

## Overview
This project implements an **Aircraft Collision Avoidance System (ACAS)** in a simulated 3D environment. The system ensures safe navigation for multiple aircraft by detecting potential conflicts and dynamically adjusting their flight paths. The implementation uses real-time monitoring, relative coordinate systems, and safety zones to evaluate and resolve collision risks effectively.

---

## Features
- **3D Simulation Environment**: Models aircraft movement in a 3D grid with integer-valued coordinates.
- **Collision Avoidance**: Dynamically avoids potential collisions based on danger and warning zones.
- **Relative Coordinate System**: Calculates avoidance maneuvers using localized reference frames.
- **Scalable Testing**: Supports multiple aircraft with diverse configurations and scenarios.
- **Logging**: Outputs simulation results to a CSV file for analysis.

---

## How It Works
1. **Safety Zones**:
   - **Danger Zone**: A 2-unit cube centered on the aircraft. Entry by another aircraft is prohibited.
   - **Warning Zone**: A 4-unit cube where intruders trigger avoidance behavior.
   
2. **Avoidance Mechanism**:
   - Aircraft establish a relative coordinate system to calculate avoidance directions.
   - Upon detecting an intruder in the warning zone, the system adjusts flight paths to maintain safe separation.

3. **Simulation**:
   - Aircraft are assigned random source and destination points.
   - Real-time monitoring updates positions and resolves conflicts until all aircraft reach their destinations.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/acas-3d.git
   cd acas-3d
