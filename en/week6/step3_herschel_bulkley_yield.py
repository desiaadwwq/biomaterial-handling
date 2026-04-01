"""
Step 3: Herschel-Bulkley Yield Stress Analysis
Analyzes pseudo-plastic fluidic behaviors (e.g. tomato paste, mayonnaise) 
that mandate a rudimentary Yield Stress threshold to induce any initial velocity flow, 
optimizing predictive tolerances via scrolling UI markers.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.widgets import Slider

# 1. Base Variables Initialization
initial_tau_y = 20.0  # Base Yield Stress (Pa)
initial_K = 5.0       # Flow Consistency Index
initial_n = 0.6       # Flow Index (Predominantly n < 1 reflecting thinning traits)

shear_rate = np.linspace(0, 100, 500)

def herschel_bulkley(gamma, tau_y, K, n):
    # \tau = \tau_y + K * \dot{\gamma}^n
    stress = np.zeros_like(gamma)
    mask = gamma > 0
    stress[mask] = tau_y + K * (gamma[mask] ** n)
    stress[~mask] = tau_y
    return stress

initial_stress = herschel_bulkley(shear_rate, initial_tau_y, initial_K, initial_n)

# 2. Master Plot UI Configurations
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.3)

line, = ax.plot(shear_rate, initial_stress, color='darkorange', lw=3, label='Herschel-Bulkley Model')
ax.set_title('Bingham Plastic / Yield-Stress Fluid Behavior', fontsize=14, fontweight='bold')
ax.set_xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
ax.set_ylabel('Shear Stress ($\\tau$, Pa)', fontsize=12)

ax.set_xlim(0, 100)
ax.set_ylim(0, 150)
ax.grid(True, linestyle='--', alpha=0.7)

# Highlight horizontal line denoting minimal break-point
hline = ax.axhline(initial_tau_y, color='red', linestyle=':', label=f'Yield Stress = {initial_tau_y} Pa')
ax.legend(loc='upper left')

# 3. Trigger Component Setup
ax_tau = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor='lightgray')
ax_n   = plt.axes([0.2, 0.08, 0.65, 0.03], facecolor='lightgray')

slider_tau = Slider(ax_tau, 'Yield Stress ($\\tau_y$)', 0.0, 50.0, valinit=initial_tau_y)
slider_n   = Slider(ax_n, 'Flow Index (n)', 0.3, 1.5, valinit=initial_n)

# 4. Asynchronous Thread Overlay
def update(val):
    c_tau_y = slider_tau.val
    c_n = slider_n.val
    
    new_stress = herschel_bulkley(shear_rate, c_tau_y, initial_K, c_n)
    
    line.set_ydata(new_stress)
    hline.set_ydata(c_tau_y)
    hline.set_label(f'Yield Stress = {c_tau_y:.1f} Pa')
    
    ax.legend(loc='upper left')
    fig.canvas.draw_idle()

slider_tau.on_changed(update)
slider_n.on_changed(update)

plt.show()
