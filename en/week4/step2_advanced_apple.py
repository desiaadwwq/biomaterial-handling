# -*- coding: utf-8 -*-
"""
Biomaterial Handling & Processing - Week 04 Lab (Advanced)
Topic: Analyzing Density and Porosity Changes with Target Swap (Apple)
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations

plt.rcParams['font.family'] = 'Segoe UI'
plt.rcParams['axes.unicode_minus'] = False

# =====================================================================
# [Advanced Assignment] Fill in the variables below with the Apple data 
# provided in the lab manual.
# =====================================================================
# Individual Apple Volume (cm^3)
volume_single_cm3 = ???  # (e.g., 315.0)

# Individual Apple Mass (g)
mass_single_g = ???      # (e.g., 280.0)

# Standard Plastic Box Volume (18,000 cm^3)
box_volume_cm3 = 40.0 * 30.0 * 15.0  

# Loaded Object Count (Apples)
apple_count = ???        # (e.g., 24)

# =====================================================================
# Density & Porosity Formulas (No modification needed below)
# =====================================================================
# 1. Particle Density
density_particle = mass_single_g / volume_single_cm3

# 2. Bulk Density
mass_total_g = mass_single_g * apple_count
density_bulk = mass_total_g / box_volume_cm3

# 3. Porosity Calculation
porosity_density_based = (1 - (density_bulk / density_particle)) * 100

print(f"[Advanced: Apple]")
print(f" - Particle Density: {density_particle:.3f} g/cm^3")
print(f" - Bulk Density    : {density_bulk:.3f} g/cm^3")
print(f" - Porosity        : {porosity_density_based:.2f} %")

# =====================================================================
# Visualization (No modification needed - Auto adapted for 24 grid)
# =====================================================================
fig = plt.figure(figsize=(18, 6))

# ---- (A) Left: 3D Virtual Packing (4x3x2 Array = 24 units) ----
ax1 = fig.add_subplot(131, projection='3d')
r = [0, 40]
for s, e in combinations(np.array(list(product(r, [0, 30], [0, 15]))), 2):
    if np.sum(np.abs(s-e)) in [40, 30, 15]:
        ax1.plot3D(*zip(s, e), color="black", linestyle='--', alpha=0.3)

x_centers = np.linspace(5, 35, 4)
y_centers = np.linspace(5, 25, 3)
z_centers = np.linspace(3.75, 11.25, 2)
X, Y, Z = np.meshgrid(x_centers, y_centers, z_centers)

# Apples visualized with a red tone
ax1.scatter(X, Y, Z, s=800, c='#FF5252', alpha=0.9, edgecolors='#B71C1C')
ax1.set_title('Advanced: Virtual Packing (24 Apples)', fontsize=14, pad=15)
ax1.set_box_aspect((40, 30, 15))

# ---- (B) Center: Density Gap Chart ----
ax2 = fig.add_subplot(132)
bars = ax2.bar(['Particle Density\n(Apple)', 'Bulk Density\n(Cargo)'], 
               [density_particle, density_bulk], color=['#FFCDD2', '#EF9A9A'], edgecolor='black', width=0.5)
ax2.set_title('Density Gap Analysis (Apple)', fontsize=14, pad=15)
ax2.set_ylim(0, max([density_particle, density_bulk]) * 1.3)
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
             f'{bar.get_height():.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# ---- (C) Right: Pie Chart ----
ax3 = fig.add_subplot(133)
ax3.pie([100 - porosity_density_based, porosity_density_based], explode=(0.05, 0),
        labels=['Apple Volume\n(Occupied)', 'Void Space\n(Porosity)'], colors=['#FFCDD2', '#e6f0ff'],
        autopct='%1.1f%%', startangle=140, textprops={'fontsize': 13, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1})
ax3.set_title(f'Volume Occupancy & Porosity ({apple_count} Units)', fontsize=14, pad=15)

plt.tight_layout()
plt.show()
