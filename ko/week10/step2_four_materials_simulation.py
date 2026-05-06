"""
10주차 실습 Step 2: 4가지 포장재/표면 조건에 따른 낙하 충격 시뮬레이션
- 맨바닥, 종이 트레이, 에어캡, 발포 스티로폼 비교
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

g = 9.81

# 각 재질별 특성 (반발 계수 e, 충돌 시간 dt)
# 1. 맨바닥
e_hard = 0.34
dt_hard = 0.005

# 2. 종이 트레이
e_tray = 0.18
dt_tray = 0.020

# 3. 에어캡
e_bubble = 0.45
dt_bubble = 0.025

# 4. 발포 스티로폼 (EPS)
e_eps = 0.30
dt_eps = 0.012

init_mass = 0.25
init_drop_height = 1.0
init_bruise_threshold = 150.0

t_total = 1.5
fps = 60
num_frames = int(t_total * fps)
time_array = np.linspace(0, t_total, num_frames)

def calc_traj(mass, drop_height, e, dt):
    v1 = -np.sqrt(2 * g * drop_height)
    v2 = abs(v1) * e
    force = mass * (v2 - v1) / dt
    t_fall = np.sqrt(2 * drop_height / g)
    
    y = np.zeros(num_frames)
    f = np.zeros(num_frames)
    
    for i, t in enumerate(time_array):
        if t < t_fall:
            y[i] = drop_height - 0.5 * g * t**2
        elif t < t_fall + dt:
            compress = (t - t_fall) / dt
            y[i] = -0.05 * np.sin(compress * np.pi)
            f[i] = force
        else:
            t_b = t - (t_fall + dt)
            y[i] = v2 * t_b - 0.5 * g * t_b**2
            if y[i] < 0: y[i] = 0
    return y, f, force

def calculate_all(mass, drop_height):
    y_h, f_h, fh_max = calc_traj(mass, drop_height, e_hard, dt_hard)
    y_t, f_t, ft_max = calc_traj(mass, drop_height, e_tray, dt_tray)
    y_b, f_b, fb_max = calc_traj(mass, drop_height, e_bubble, dt_bubble)
    y_e, f_e, fe_max = calc_traj(mass, drop_height, e_eps, dt_eps)
    return y_h, y_t, y_b, y_e, f_h, f_t, f_b, f_e, fh_max, ft_max, fb_max, fe_max

y_h, y_t, y_b, y_e, f_h, f_t, f_b, f_e, fh_max, ft_max, fb_max, fe_max = calculate_all(init_mass, init_drop_height)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
fig.subplots_adjust(bottom=0.35)
fig.suptitle('[시뮬레이션] 4가지 표면 조건 낙하 충격 비교', fontsize=18, fontweight='bold')

# 애니메이션 축
ax1.set_xlim(-0.5, 3.5)
ax1.set_ylim(-0.15, 2.2)
ax1.set_xticks([0, 1, 2, 3])
ax1.set_xticklabels(['맨바닥', '종이 트레이', '에어캡', '스티로폼'], fontsize=11)
ax1.set_ylabel('높이 (m)', fontsize=12)
ax1.set_title('낙하 및 반발 애니메이션', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.6)

ax1.axhline(0, color='black', linewidth=3)
# 완충재 바닥 시각화
ax1.axhline(-0.05, xmin=0.3, xmax=0.45, color='green', linewidth=10, alpha=0.5) # 트레이
ax1.axhline(-0.05, xmin=0.55, xmax=0.7, color='blue', linewidth=10, alpha=0.3) # 에어캡
ax1.axhline(-0.05, xmin=0.8, xmax=0.95, color='orange', linewidth=10, alpha=0.5) # 스티로폼

apple_h, = ax1.plot([], [], 'ro', markersize=15, label='맨바닥')
apple_t, = ax1.plot([], [], 'go', markersize=15, label='종이 트레이')
apple_b, = ax1.plot([], [], 'bo', markersize=15, label='에어캡')
apple_e, = ax1.plot([], [], color='orange', marker='o', markersize=15, linestyle='None', label='스티로폼')
ax1.legend(loc='upper right', fontsize=9)

# 충격력 축
ax2.set_xlim(0, t_total)
ax2.set_ylim(0, 900)
ax2.set_xlabel('시간 (s)', fontsize=12)
ax2.set_ylabel('충격력 (N)', fontsize=12)
ax2.set_title('시간에 따른 충격력 변화', fontsize=14)
ax2.grid(True, linestyle='--', alpha=0.6)

thresh_line = ax2.axhline(init_bruise_threshold, color='red', linestyle='--', linewidth=2, label=f'멍 한계 ({init_bruise_threshold}N)')
line_f_h, = ax2.plot([], [], 'r-', linewidth=2, label='맨바닥')
line_f_t, = ax2.plot([], [], 'g-', linewidth=2, label='종이 트레이')
line_f_b, = ax2.plot([], [], 'b-', linewidth=2, label='에어캡')
line_f_e, = ax2.plot([], [], color='orange', linestyle='-', linewidth=2, label='스티로폼')
ax2.legend(loc='upper right', fontsize=9)

# 정보 텍스트 박스
info_text = ax2.text(0.05, 0.65, '', transform=ax2.transAxes, fontsize=11, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="gray", lw=2, alpha=0.8))

axcolor = 'lightgray'
ax_mass = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_height = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_thresh = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

s_mass = Slider(ax_mass, '사과 질량 (kg)', 0.1, 0.5, valinit=init_mass, valstep=0.01)
s_height = Slider(ax_height, '낙하 높이 (m)', 0.5, 2.0, valinit=init_drop_height, valstep=0.1)
s_thresh = Slider(ax_thresh, '손상 임계치 (N)', 50, 800, valinit=init_bruise_threshold, valstep=10)

btn_ax = plt.axes([0.85, 0.15, 0.1, 0.08])
btn_restart = Button(btn_ax, '다시 재생\n(Restart)', hovercolor='white')

current_frame = [0]

def update_sliders(val=None):
    global y_h, y_t, y_b, y_e, f_h, f_t, f_b, f_e
    m = s_mass.val
    h = s_height.val
    thresh = s_thresh.val
    
    y_h, y_t, y_b, y_e, f_h, f_t, f_b, f_e, fh_max, ft_max, fb_max, fe_max = calculate_all(m, h)
    
    thresh_line.set_ydata([thresh, thresh])
    thresh_line.set_label(f'멍 한계 ({thresh:.0f}N)')
    ax2.legend(loc='upper right', fontsize=9)
    
    text = f"[최대 충격력 결과]\n"
    text += f"맨바닥: {fh_max:.1f} N {'(손상 ❌)' if fh_max > thresh else '(안전 ⭕)'}\n"
    text += f"종이 트레이: {ft_max:.1f} N {'(손상 ❌)' if ft_max > thresh else '(안전 ⭕)'}\n"
    text += f"에어캡: {fb_max:.1f} N {'(손상 ❌)' if fb_max > thresh else '(안전 ⭕)'}\n"
    text += f"스티로폼: {fe_max:.1f} N {'(손상 ❌)' if fe_max > thresh else '(안전 ⭕)'}"
    
    info_text.set_text(text)
    current_frame[0] = 0

s_mass.on_changed(update_sliders)
s_height.on_changed(update_sliders)
s_thresh.on_changed(update_sliders)

def restart_anim(event):
    current_frame[0] = 0

btn_restart.on_clicked(restart_anim)

update_sliders()

def frame_generator():
    while True:
        yield current_frame[0]
        if current_frame[0] < num_frames - 1:
            current_frame[0] += 1

def update_anim(f):
    apple_h.set_data([0], [y_h[f]])
    apple_t.set_data([1], [y_t[f]])
    apple_b.set_data([2], [y_b[f]])
    apple_e.set_data([3], [y_e[f]])
    
    line_f_h.set_data(time_array[:f+1], f_h[:f+1])
    line_f_t.set_data(time_array[:f+1], f_t[:f+1])
    line_f_b.set_data(time_array[:f+1], f_b[:f+1])
    line_f_e.set_data(time_array[:f+1], f_e[:f+1])
    
    return apple_h, apple_t, apple_b, apple_e, line_f_h, line_f_t, line_f_b, line_f_e, thresh_line, info_text

ani = animation.FuncAnimation(
    fig, update_anim, frames=frame_generator, 
    interval=1000/fps, blit=False, cache_frame_data=False
)

plt.show()
