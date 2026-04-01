"""
Step 1: Power Law Model Curve Fitting
This script computes the fundamental coefficients for the Power Law model (Tau = K * Gamma^n)
of Non-Newtonian fluids, specifically the Consistency Index (K) and Flow Behavior Index (n).
It models hypothetical Shear Rate and Shear Stress data utilizing scipy.optimize.curve_fit.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from scipy.optimize import curve_fit

# 1. Hypothetical Experimental Data Array (Assuming Pseudoplastic Starch Paste)
# Shear Rate (1/s): 10 ~ 100
shear_rate_data = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
# Shear Stress (Pa) measurements
shear_stress_data = np.array([18.5, 29.3, 38.5, 46.8, 54.3, 61.2, 67.8, 74.0, 80.0, 85.8])

# 2. Define Power Law Mathematical Function
# Equation: \tau = K * \dot{\gamma}^n
def power_law(gamma, K, n):
    return K * (gamma ** n)

# 3. Executive Curve Fitting Process
# popt: Optimal tracking parameter array [K, n]
# pcov: Covariance bounds array
popt, pcov = curve_fit(power_law, shear_rate_data, shear_stress_data)

K_est, n_est = popt
print(f"--- Power Law Fit Coordinates ---")
print(f"Consistency Index (K): {K_est:.4f} Pa·s^n")
print(f"Flow Behavior Index (n): {n_est:.4f}")

# 4. Result Diagram Plotting
shear_rate_smooth = np.linspace(0, 100, 200)
shear_stress_fit = power_law(shear_rate_smooth, K_est, n_est)

plt.figure(figsize=(8, 6))

# Experimental Data Tracker Scatter Map
plt.scatter(shear_rate_data, shear_stress_data, color='blue', label='Experimental Data (Starch Paste)', s=50, zorder=3)

# Fitted Trend-line Regression Trajectory
plt.plot(shear_rate_smooth, shear_stress_fit, color='red', linewidth=2, label=rf'Power Law Fit ($\tau = {K_est:.2f} \cdot \dot{{\gamma}}^{{{n_est:.2f}}}$)', zorder=2)

plt.title('Non-Newtonian Fluid: Power Law Curve Fitting', fontsize=14, fontweight='bold')
plt.xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
plt.ylabel('Shear Stress ($\\tau$, Pa)', fontsize=12)
plt.xlim(0, 110)
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=11)

plt.tight_layout()
plt.show()
