"""
Step 2: Apparent Viscosity Dynamics Simulation
This script triggers responsive animations of Apparent Viscosity under dynamic shear rates
for respective Non-Newtonian classifications (Pseudoplastic, Newtonian, Dilatant),
empowered by manipulating the structural Flow Index (n) slider UI.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.widgets import Slider

# 1. Base Parameter Declarations
initial_K = 10.0   # Base Consistency Index (Pa·s^n)
initial_n = 0.5    # Base Flow Index (Pseudoplastic)

shear_rate = np.linspace(0.1, 100, 500)  # Offset from 0.0 to prevent division zero bounds

def calc_apparent_viscosity(K, n, gamma):
    # \eta = \frac{\tau}{\dot{\gamma}} = K \cdot \dot{\gamma}^{n-1}
    return K * (gamma ** (n - 1))

# Generating baseline payload array
app_viscosity = calc_apparent_viscosity(initial_K, initial_n, shear_rate)

# 2. Blueprint Rendering UI Layout
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)

# Trajectory Plot Render
line, = ax.plot(shear_rate, app_viscosity, color='purple', lw=3)
ax.set_title(f"Apparent Viscosity vs Shear Rate (n = {initial_n:.2f})", fontsize=14, fontweight='bold')
ax.set_xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
ax.set_ylabel('Apparent Viscosity ($\eta$, Pa·s)', fontsize=12)

ax.set_ylim(0, 50)
ax.set_xlim(0, 100)
ax.grid(True, linestyle='--', alpha=0.7)

# Asymptotic baseline boundary
ax.axhline(initial_K, color='gray', linestyle=':', label='n=1.0 (Newtonian) Reference')
ax.legend()

# 3. Controller UI Integration
ax_n = plt.axes([0.15, 0.1, 0.70, 0.03], facecolor='lightgoldenrodyellow')
slider_n = Slider(
    ax=ax_n,
    label='Flow Index (n)',
    valmin=0.2,   # Lethal Shear Thinning Range
    valmax=1.8,   # Solidification Shear Thickening Range
    valinit=initial_n,
    valstep=0.05
)

def get_fluid_type(n_val):
    if n_val < 0.95: return "Pseudoplastic (Shear Thinning)"
    elif n_val > 1.05: return "Dilatant (Shear Thickening)"
    else: return "Newtonian Fluid"

# 4. Trigger Override Callback
def update(val):
    current_n = slider_n.val
    
    # Live algorithmic regeneration
    new_viscosity = calc_apparent_viscosity(initial_K, current_n, shear_rate)
    
    line.set_ydata(new_viscosity)
    ax.set_title(f"{get_fluid_type(current_n)}: Apparent Viscosity Dynamics (n = {current_n:.2f})", fontsize=14, fontweight='bold')
    
    if current_n > 1.05:
        ax.set_ylim(0, max(new_viscosity) + 10)
    elif current_n < 0.95:
        ax.set_ylim(0, 50)
    else:
        ax.set_ylim(0, 20)
        
    fig.canvas.draw_idle()

slider_n.on_changed(update)

plt.show()
