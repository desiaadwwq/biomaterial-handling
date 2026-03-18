# -*- coding: utf-8 -*-
"""
생물자원가공공학 및 실습 4주차 심화
주제: 형상(Shape)에 따른 공극률의 극단적 차이 비교 (토마토 vs 바나나)
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations

# 폰트
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

box_w, box_d, box_h = 40.0, 30.0, 15.0
box_volume = box_w * box_d * box_h

# =====================================================================
# 1. 토마토 (Tomato - 완전 구형)
# =====================================================================
tomato_vol = 160.0 # cm^3
tomato_mass = 150.0 # g
tomato_count = 60  # 규칙적으로 예쁘게 60개까지 적재 가능

tomato_density_p = tomato_mass / tomato_vol
tomato_density_b = (tomato_mass * tomato_count) / box_volume
tomato_porosity = (1 - (tomato_density_b / tomato_density_p)) * 100

# 반경 계산
R_tomato = np.cbrt(tomato_vol * (3 / (4 * np.pi)))

# 구형 규칙 배열 (벌집처럼 촘촘하게 쌓이는 시뮬레이션)
tomato_positions = []
z = R_tomato
layer = 0
while len(tomato_positions) < tomato_count and z <= box_h:
    y = R_tomato
    while y <= box_d and len(tomato_positions) < tomato_count:
        x = R_tomato + (layer % 2) * R_tomato
        while x <= box_w and len(tomato_positions) < tomato_count:
            tomato_positions.append([x, y, z])
            x += 2 * R_tomato
        y += 2 * R_tomato
    z += 2 * R_tomato * 0.9  # 살짝 겹쳐지듯 촘촘하게
    layer += 1
tomato_positions = np.array(tomato_positions)

# =====================================================================
# 2. 바나나 (Banana - 비대칭형, 긴 타원체)
# =====================================================================
banana_vol = 140.0 # cm^3
banana_mass = 130.0 # g
# 바나나는 서로 얽혀서 커다란 틈을 만들기 때문에 60개가 절대 못들어가고 대략 30~35개 한계
banana_count = 35 

banana_density_p = banana_mass / banana_vol
banana_density_b = (banana_mass * banana_count) / box_volume
banana_porosity = (1 - (banana_density_b / banana_density_p)) * 100

# 바나나는 길이가 길어(약 18cm) 차지하는 X축 공간이 크고 듬성듬성 채우게 됨
Rx, Ry, Rz = 9.0, 2.0, 2.0 

banana_positions = []
z_b = Rz + 1.0
while len(banana_positions) < banana_count and z_b <= box_h:
    y_b = Ry + 2.0
    while y_b <= box_d and len(banana_positions) < banana_count:
        x_b = Rx + 2.0
        while x_b <= box_w and len(banana_positions) < banana_count:
            # 듬성듬성 거대한 공극(Macro-voids) 생성
            banana_positions.append([x_b, y_b, z_b])
            # 무작위로 살짝 틀어지고 겹침 (불규칙함 극대화)
            x_b += Rx * 1.8 + np.random.uniform(0, 3) 
        y_b += Ry * 4.0 + np.random.uniform(0, 3)
    z_b += Rz * 2.5 + np.random.uniform(0, 2)
banana_positions = np.array(banana_positions)


# =====================================================================
# 시각화 (두 농산물의 형태론적 차이 표면 렌더링 방식)
# =====================================================================
fig = plt.figure(figsize=(16, 7))

# --- [A] 좌측: 둥근 토마토 ---
ax1 = fig.add_subplot(121, projection='3d')
for s, e in combinations(np.array(list(product([0, box_w], [0, box_d], [0, box_h]))), 2):
    if np.sum(np.abs(s-e)) in [box_w, box_d, box_h]:
        ax1.plot3D(*zip(s, e), color="black", linestyle='-', alpha=0.3)

# 토마토 곡면(Surface) 그리기 함수
def draw_tomato(ax, cx, cy, cz, R):
    u = np.linspace(0, 2 * np.pi, 12)
    v = np.linspace(0, np.pi, 10)
    X = R * np.outer(np.cos(u), np.sin(v))
    Y = R * np.outer(np.sin(u), np.sin(v))
    Z = R * 0.9 * np.outer(np.ones(np.size(u)), np.cos(v)) # 위아래가 약간 납작한 형태
    ax.plot_surface(X + cx, Y + cy, Z + cz, color='tomato', alpha=0.9, edgecolor='brown', linewidth=0.1)

if len(tomato_positions) > 0:
    for (cx, cy, cz) in tomato_positions:
        draw_tomato(ax1, cx, cy, cz, R_tomato)

ax1.set_xlim([0, box_w])
ax1.set_ylim([0, box_d])
ax1.set_zlim([0, box_h])
ax1.set_box_aspect((box_w, box_d, box_h))
ax1.set_title(f'토마토 (현실적 표면 렌더링)\n예상 공극률: {tomato_porosity:.1f}%', fontsize=15, pad=20, fontweight='bold', color='#B22222')
ax1.view_init(elev=20, azim=35)

# --- [B] 우측: 길쭉한 바나나 ---
ax2 = fig.add_subplot(122, projection='3d')
for s, e in combinations(np.array(list(product([0, box_w], [0, box_d], [0, box_h]))), 2):
    if np.sum(np.abs(s-e)) in [box_w, box_d, box_h]:
        ax2.plot3D(*zip(s, e), color="black", linestyle='-', alpha=0.3)

# 3D 회전 행렬 생성 함수
def roty(angle):
    return np.array([[np.cos(angle), 0, np.sin(angle)],
                     [0, 1, 0],
                     [-np.sin(angle), 0, np.cos(angle)]])
def rotz(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0],
                     [np.sin(angle), np.cos(angle), 0],
                     [0, 0, 1]])

# 바나나 휘어진 3D 표면 그리기 함수
def draw_banana(ax, cx, cy, cz, rx, ry, rz):
    u = np.linspace(0, 2 * np.pi, 12)
    v = np.linspace(0, np.pi, 10)
    # 1. 뼈대 타원체
    X0 = rx * np.outer(np.cos(u), np.sin(v))
    Y0 = ry * np.outer(np.sin(u), np.sin(v))
    Z0 = rz * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # 2. 바나나처럼 휘게 만들기 (포물선 형태 구부림)
    Z0 = Z0 + 0.04 * (X0**2) - (0.04 * rx**2)/2
    
    # 3. 무작위 3D 각도 회전
    ang_y = np.random.uniform(0, 2*np.pi)
    ang_z = np.random.uniform(0, 2*np.pi)
    Ry_mat = roty(ang_y)
    Rz_mat = rotz(ang_z)
    R_total = Rz_mat @ Ry_mat
    
    shape = X0.shape
    pts = np.vstack((X0.flatten(), Y0.flatten(), Z0.flatten()))
    rotated_pts = R_total @ pts
    
    X_rot = rotated_pts[0,:].reshape(shape) + cx
    Y_rot = rotated_pts[1,:].reshape(shape) + cy
    Z_rot = rotated_pts[2,:].reshape(shape) + cz
    
    ax.plot_surface(X_rot, Y_rot, Z_rot, color='#FFD700', alpha=0.9, edgecolor='goldenrod', linewidth=0.2)

if len(banana_positions) > 0:
    for (cx, cy, cz) in banana_positions:
        draw_banana(ax2, cx, cy, cz, Rx, Ry, Rz)

# 커다란 빈 공간(Macro-voids) 표기
ax2.text(20, 15, 10, '무작위 다발적 얽힘으로\n통풍 문제(Macro-voids) 확실시 발생', color='blue', fontsize=12, ha='center', fontweight='bold', zorder=10)

ax2.set_xlim([0, box_w])
ax2.set_ylim([0, box_d])
ax2.set_zlim([0, box_h])
ax2.set_box_aspect((box_w, box_d, box_h))
ax2.set_title(f'바나나 (현실적 표면 렌더링)\n예상 공극률: {banana_porosity:.1f}% (거대 빈틈)', fontsize=15, pad=20, fontweight='bold', color='#DAA520')
ax2.view_init(elev=20, azim=35)

# 전체 레이아웃
plt.suptitle('농산물 형상(Shape)에 따른 체적 점유와 거대 공극 발생 3D 표면 실증', fontsize=18, fontweight='bold')
fig.tight_layout()
fig.subplots_adjust(top=0.85)

plt.show()
