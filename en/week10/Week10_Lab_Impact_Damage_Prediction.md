# Week 10 Lab: Impact Characteristics & Damage Prediction Modeling

## 🎯 Lab Overview

- **Objective**: Analyze the impact behavior of biomaterials using the open-source physics analysis tool (Tracker) and Python to determine the critical damage threshold.
- **Activity**: Video motion tracking-based velocity and acceleration data extraction, followed by calculation of the coefficient of restitution and impact force.
- **Algorithm Focus**: Tracking positional changes per frame → Deriving falling velocity and coefficient of restitution → Evaluating damage prevention (energy absorption) across different packaging material thicknesses.

---

## 🛠 [Step 0] Environment Setup & Tracker Basics

### Required Tools
- **[Tracker](https://physlets.org/tracker/)**: Free, open-source video analysis and motion tracking software.
- **Python Packages**: `numpy` and `matplotlib` for parsing and visualizing CSV data exported from Tracker.

### Data Preparation
- Target: Fruit free-fall experimental video (dropping from different heights onto various surfaces).
- **Calibration Stick**: Essential for converting pixel dimensions into real-world physical units (e.g., meters).
- **Tracking & Export**: Track the object's center of mass, then export the `time-vs-y_position` and `time-vs-y_velocity` data to a CSV format.

---

## 💻 [Step 1] Coefficient of Restitution & Maximum Impact Force (`step1_impact_analysis.py`)

### Lab Objectives
- Calculate the Coefficient of Restitution ($e$) based on the velocity just before impact ($v_1$) and immediately after rebound ($v_2$).
- Compute the maximum Impact Force based on the collision duration ($\Delta t$) and compare it with the damage threshold.

### Working Principles
- Load the extracted Tracker CSV data and analyze the time-series velocity changes.
- Calculate $e = |v_2 / v_1|$ — Quantifies the elastic and energy absorption characteristics of the surface material.
- Calculate maximum impact force using the momentum change $\Delta p = m(v_2 - v_1)$ and the impulse equation $I = F \Delta t$.

### Industrial Considerations
- **Cushioning Effect**: Inserting foam packaging extends the collision time ($\Delta t$), verifying a dramatic reduction in the maximum impact force ($F$).
- **Damage Prediction Modeling**: If the calculated impact energy exceeds the target biomaterial's energy absorption limit (Bio-yield), internal bruising is predicted.
