"""
Week 10 Lab Step 1: Fruit Free-Fall Impact Characteristics & Restitution Analysis (Interactive Simulation)
- Calculate the coefficient of restitution using pre- and post-impact velocities based on mock Tracker data.
- Dynamic adjustment of mass, drop height, and damage threshold via Sliders.
- Compare maximum impact forces with and without cushioning material and simulate damage.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import matplotlib.font_manager as fm

# =====================================================================
# 1. Physical Parameters and Constants
# =====================================================================
g = 9.81  # Gravitational acceleration (m/s^2)

# Coefficient of Restitution derived from Tracker data (Fixed values)
# Hard surface: v1 = 4.40, v2 = 1.50 -> e = 0.34
# Soft surface: v1 = 4.40, v2 = 0.80 -> e = 0.18
e_hard = 1.50 / 4.40
e_soft = 0.80 / 4.40

# Collision Duration Time
dt_hard = 0.005  # s
dt_soft = 0.020  # s

# Initial State Variables
init_mass = 0.25
init_drop_height = 1.0
init_bruise_threshold = 150.0

# =====================================================================
# 2. Simulation Data Calculation Function
# =====================================================================
t_total = 1.5  # Total simulation time (fixed for max 2.0m drop)
fps = 60
num_frames = int(t_total * fps)
time_array = np.linspace(0, t_total, num_frames)

def calculate_data(mass, drop_height):
    v1 = -np.sqrt(2 * g * drop_height)
    v2_hard = abs(v1) * e_hard
    v2_soft = abs(v1) * e_soft
    
    force_hard = mass * (v2_hard - v1) / dt_hard
    force_soft = mass * (v2_soft - v1) / dt_soft
    
    t_fall = np.sqrt(2 * drop_height / g)
    
    y_h = np.zeros(num_frames)
    y_s = np.zeros(num_frames)
    f_h = np.zeros(num_frames)
    f_s = np.zeros(num_frames)
    
    for i, t in enumerate(time_array):
        # Hard Surface
        if t < t_fall:
            y_h[i] = drop_height - 0.5 * g * t**2
        elif t < t_fall + dt_hard:
            y_h[i] = 0
            f_h[i] = force_hard
        else:
            t_b = t - (t_fall + dt_hard)
            y_h[i] = v2_hard * t_b - 0.5 * g * t_b**2
            if y_h[i] < 0: y_h[i] = 0
            
        # Soft Surface
        if t < t_fall:
            y_s[i] = drop_height - 0.5 * g * t**2
        elif t < t_fall + dt_soft:
            compress = (t - t_fall) / dt_soft
            y_s[i] = -0.05 * np.sin(compress * np.pi)
            f_s[i] = force_soft
        else:
            t_b = t - (t_fall + dt_soft)
            y_s[i] = v2_soft * t_b - 0.5 * g * t_b**2
            if y_s[i] < 0: y_s[i] = 0
            
    return y_h, y_s, f_h, f_s, force_hard, force_soft

# Initial calculation
y_hard, y_soft, f_hard, f_soft, fh_max, fs_max = calculate_data(init_mass, init_drop_height)

# =====================================================================
# 3. Plot and GUI Layout Setup
# =====================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
fig.subplots_adjust(bottom=0.35)  # Space for sliders
fig.suptitle('[Simulation] Fruit Drop Impact Interactive Analysis', fontsize=16, fontweight='bold')

# --- 1) Drop Animation Axis ---
ax1.set_xlim(-1, 3)
ax1.set_ylim(-0.15, 2.2)  # Max height 2.0m
ax1.set_xticks([0, 2])
ax1.set_xticklabels(['Hard Surface', 'Soft Surface'], fontsize=12)
ax1.set_ylabel('Height (m)', fontsize=12)
ax1.set_title('Drop and Rebound Animation', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.6)

# Surface and pad visualization
ax1.axhline(0, color='black', linewidth=3)
ax1.axhline(-0.05, xmin=0.6, xmax=0.9, color='lightgreen', linewidth=10, alpha=0.5)

apple_hard, = ax1.plot([], [], 'ro', markersize=20, label='Apple (Hard)')
apple_soft, = ax1.plot([], [], 'go', markersize=20, label='Apple (Soft)')
ax1.legend(loc='upper right')

# --- 2) Impact Force Graph Axis ---
ax2.set_xlim(0, t_total)
ax2.set_ylim(0, 900)  # Max possible force
ax2.set_xlabel('Time (s)', fontsize=12)
ax2.set_ylabel('Impact Force (N)', fontsize=12)
ax2.set_title('Impact Force over Time', fontsize=14)
ax2.grid(True, linestyle='--', alpha=0.6)

thresh_line = ax2.axhline(init_bruise_threshold, color='red', linestyle='--', linewidth=2, label=f'Bruise Threshold ({init_bruise_threshold}N)')
line_f_hard, = ax2.plot([], [], 'r-', linewidth=3, label='Hard Surface Force')
line_f_soft, = ax2.plot([], [], 'g-', linewidth=3, label='Soft Surface Force')
ax2.legend(loc='upper right')

# Text Info Boxes
bbox_props_hard = dict(boxstyle="round,pad=0.5", fc="white", ec="red", lw=2, alpha=0.8)
bbox_props_soft = dict(boxstyle="round,pad=0.5", fc="white", ec="green", lw=2, alpha=0.8)

txt_hard = ax2.text(0.05, 0.85, '', transform=ax2.transAxes, fontsize=12, fontweight='bold', bbox=bbox_props_hard)
txt_soft = ax2.text(0.05, 0.70, '', transform=ax2.transAxes, fontsize=12, fontweight='bold', bbox=bbox_props_soft)

# =====================================================================
# 4. UI Controls (Sliders and Buttons)
# =====================================================================
axcolor = 'lightgray'
ax_mass = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_height = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_thresh = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

s_mass = Slider(ax_mass, 'Apple Mass (kg)', 0.1, 0.5, valinit=init_mass, valstep=0.01)
s_height = Slider(ax_height, 'Drop Height (m)', 0.5, 2.0, valinit=init_drop_height, valstep=0.1)
s_thresh = Slider(ax_thresh, 'Damage Threshold (N)', 50, 800, valinit=init_bruise_threshold, valstep=10)

btn_ax = plt.axes([0.85, 0.15, 0.1, 0.08])
btn_restart = Button(btn_ax, 'Restart\nAnimation', hovercolor='white')

current_frame = [0]

def update_sliders(val=None):
    global y_hard, y_soft, f_hard, f_soft
    m = s_mass.val
    h = s_height.val
    thresh = s_thresh.val
    
    # Recalculate with new values
    y_hard, y_soft, f_hard, f_soft, fh, fs = calculate_data(m, h)
    
    # Update threshold line
    thresh_line.set_ydata([thresh, thresh])
    thresh_line.set_label(f'Bruise Threshold ({thresh:.0f}N)')
    ax2.legend(loc='upper right')
    
    # Update text boxes
    txt_hard.set_text(f"Hard Surface Max Force: {fh:.1f} N\n({'Damage Risk (X)' if fh > thresh else 'Safe (O)'})")
    txt_hard.set_color('darkred' if fh > thresh else 'darkgreen')
    
    txt_soft.set_text(f"Soft Surface Max Force: {fs:.1f} N\n({'Damage Risk (X)' if fs > thresh else 'Safe (O)'})")
    txt_soft.set_color('darkred' if fs > thresh else 'darkgreen')
    
    # Reset animation
    current_frame[0] = 0

# Connect events
s_mass.on_changed(update_sliders)
s_height.on_changed(update_sliders)
s_thresh.on_changed(update_sliders)

def restart_anim(event):
    current_frame[0] = 0

btn_restart.on_clicked(restart_anim)

# Apply initial text setup
update_sliders()

# =====================================================================
# 5. Animation Loop
# =====================================================================
def frame_generator():
    while True:
        yield current_frame[0]
        # Stop at the last frame
        if current_frame[0] < num_frames - 1:
            current_frame[0] += 1

def update_anim(f):
    apple_hard.set_data([0], [y_hard[f]])
    apple_soft.set_data([2], [y_soft[f]])
    
    line_f_hard.set_data(time_array[:f+1], f_hard[:f+1])
    line_f_soft.set_data(time_array[:f+1], f_soft[:f+1])
    
    return apple_hard, apple_soft, line_f_hard, line_f_soft, thresh_line, txt_hard, txt_soft

ani = animation.FuncAnimation(
    fig, update_anim, frames=frame_generator, 
    interval=1000/fps, blit=False, cache_frame_data=False
)

plt.show()
