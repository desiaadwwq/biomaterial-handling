import numpy as np
import matplotlib.pyplot as plt
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 상수 설정
g = 9.81
drop_height = 1.0  # m
mass = 0.25  # kg
v1 = -np.sqrt(2 * g * drop_height)  # -4.429 m/s

# 재질 파라미터 (e, dt)
e_hard, dt_hard = 0.34, 0.005
e_tray, dt_tray = 0.18, 0.020
e_bubble, dt_bubble = 0.45, 0.025
e_eps, dt_eps = 0.30, 0.012

t_fall = np.sqrt(2 * drop_height / g)
t_total = 1.0
time_array = np.linspace(0, t_total, 2000)

def calc_traj(e, dt):
    v2 = abs(v1) * e
    y = np.zeros_like(time_array)
    a = np.zeros_like(time_array)
    for i, t in enumerate(time_array):
        if t < t_fall:
            y[i] = drop_height - 0.5 * g * t**2
            a[i] = -g
        elif t < t_fall + dt:
            compress = (t - t_fall) / dt
            y[i] = -0.05 * np.sin(compress * np.pi)
            a[i] = (v2 - v1) / dt
        else:
            t_b = t - (t_fall + dt)
            y[i] = v2 * t_b - 0.5 * g * t_b**2
            a[i] = -g
            if y[i] < 0: 
                y[i] = 0
                a[i] = 0
    return y, a

y_h, a_h = calc_traj(e_hard, dt_hard)
y_t, a_t = calc_traj(e_tray, dt_tray)
y_b, a_b = calc_traj(e_bubble, dt_bubble)
y_e, a_e = calc_traj(e_eps, dt_eps)

os.makedirs('ko/week10/images', exist_ok=True)

# 1. 위치-시간 그래프
plt.figure(figsize=(10, 6))
plt.plot(time_array, y_h, 'r-', lw=2, label='맨바닥')
plt.plot(time_array, y_t, 'g-', lw=2, label='종이 트레이')
plt.plot(time_array, y_b, 'b--', lw=2, label='에어캡')
plt.plot(time_array, y_e, color='orange', linestyle='-.', lw=2, label='발포 스티로폼')
plt.axhline(0, color='black', lw=1, linestyle='--')
plt.title('4가지 포장재 낙하 위치-시간 (Position-Time) 비교', fontsize=16, fontweight='bold')
plt.xlabel('시간 (s)', fontsize=12)
plt.ylabel('위치 y (m)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('ko/week10/images/tracker_position_time_4m.png', dpi=300)
plt.close()

# 2. 가속도-시간 그래프
plt.figure(figsize=(10, 6))
plt.plot(time_array, a_h, 'r-', lw=2, label='맨바닥')
plt.plot(time_array, a_t, 'g-', lw=2, label='종이 트레이')
plt.plot(time_array, a_b, 'b--', lw=2, label='에어캡')
plt.plot(time_array, a_e, color='orange', linestyle='-.', lw=2, label='발포 스티로폼')
plt.title('4가지 포장재 가속도-시간 (Acceleration-Time) 비교', fontsize=16, fontweight='bold')
plt.xlabel('시간 (s)', fontsize=12)
plt.ylabel('가속도 a (m/s²)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('ko/week10/images/tracker_acceleration_time_4m.png', dpi=300)
plt.close()
