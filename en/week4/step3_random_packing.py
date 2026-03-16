import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

print("-" * 50)
print("🥑 Step 3: Packing Simulation Comparison (Ordered vs. Random)")
print("-" * 50)

# 1. Simulation Environment & Produce Specifications 
box_length = 40.0
box_width = 30.0
box_height = 15.0
box_vol = box_length * box_width * box_height

# Calculate equivalent radius assuming perfect sphere based on average avocado volume (205.4 cm³)
volume_single_cm3 = 205.4
radius = (3 * volume_single_cm3 / (4 * np.pi)) ** (1/3) # approx. 3.66 cm

max_items = 45 # Target produce count from baseline lab

def generate_ordered_packing():
    """Ordered Packing - Ideal regular arrangement utilizing an orthogonal grid"""
    x_positions = np.linspace(radius, box_length - radius, 5)
    y_positions = np.linspace(radius, box_width - radius, 3)
    z_positions = np.linspace(radius, box_height - radius, 3)
    
    positions = []
    for z in z_positions:
        for y in y_positions:
            for x in x_positions:
                positions.append([x, y, z])
                if len(positions) == max_items:
                    return np.array(positions)
    return np.array(positions)

def generate_random_packing():
    """Random Packing - Integrating Monte Carlo randomness with Collision Detection"""
    positions = []
    max_attempts = 100000 # Max algorithmic iterations to prevent locking
    attempts = 0
    
    np.random.seed(42) # Fixed seed for reproducibility
    
    while len(positions) < max_items and attempts < max_attempts:
        # Generate random centroid so spherical bounds don't clip through the box
        x = np.random.uniform(radius, box_length - radius)
        y = np.random.uniform(radius, box_width - radius)
        z = np.random.uniform(radius, box_height - radius)
        new_pos = np.array([x, y, z])
        
        if len(positions) == 0:
            positions.append(new_pos)
        else:
            # Check spatial distance against all currently verified fruits (using scipy cdist)
            # Collision-free iff the distance is strictly greater than diameter (2*radius)
            dists = cdist([new_pos], positions)[0]
            if np.all(dists >= 2 * radius):
                positions.append(new_pos)
        
        attempts += 1
        
    return np.array(positions), attempts

# Execute array computations
ordered_pos = generate_ordered_packing()
random_pos, attempts_needed = generate_random_packing()

# Verbose Logging
print(f"[Ordered Packing] Successfully fitted objects: {len(ordered_pos)}/{max_items}")
print(f"[Random Packing] Successfully fitted objects: {len(random_pos)}/{max_items}")
print(f"   -> Algorithm iteration cycles: {attempts_needed} loops\n")

if len(random_pos) < max_items:
    print("💡 [Analytical Insight] In Random Packing, chaotic void distributions")
    print("   splinter the available volume into unusable fractured airspace, preventing")
    print("   100% capacity fitting even within identical global parameters.")
    print("   This fundamentally visualizes why 'Bulk Density' drastically drops in practice.\n")

# 2. 3D Visualization Comparison Panel
fig = plt.figure(figsize=(14, 6))

def plot_packing(ax, positions, title):
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlim([0, box_length])
    ax.set_ylim([0, box_width])
    ax.set_zlim([0, box_height])
    ax.set_xlabel("X (cm)")
    ax.set_ylabel("Y (cm)")
    ax.set_zlabel("Z (cm)")
    
    # Constructing wireframe box boundaries
    for s, e in [((0,0,0),(0,box_width,0)), ((0,0,0),(0,0,box_height)), ((0,box_width,0),(0,box_width,box_height)),
                 ((0,0,box_height),(0,box_width,box_height)), ((box_length,0,0),(box_length,box_width,0)),
                 ((box_length,0,0),(box_length,0,box_height)), ((box_length,box_width,0),(box_length,box_width,box_height)),
                 ((box_length,0,box_height),(box_length,box_width,box_height)),
                 ((0,0,0),(box_length,0,0)), ((0,box_width,0),(box_length,box_width,0)),
                 ((0,0,box_height),(box_length,0,box_height)), ((0,box_width,box_height),(box_length,box_width,box_height))]:
        ax.plot3D(*zip(s,e), color='black', linewidth=1, alpha=0.5)
        
    # Scatter rendering as idealized spheres
    if len(positions) > 0:
        ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], 
                   s=1800, c='#4A90E2', alpha=0.8, edgecolors='#333333', linewidth=1.5)

# Left Panel: Ordered Grid
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
plot_packing(ax1, ordered_pos, "Ordered Packing (Grid: 45 units)")

# Right Panel: Random Chaos
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
plot_packing(ax2, random_pos, f"Random Packing (Fitted: {len(random_pos)} units)")

plt.tight_layout()
plt.show()
