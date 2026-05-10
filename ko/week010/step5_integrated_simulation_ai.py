"""
10주차 실습 Step 5: 통합 시뮬레이터 (물리 역학 + 머신러닝 AI)
- Step 2의 '물리 낙하 시뮬레이션(애니메이션)'과 
- Step 3의 'AI 파손 확률 예측 모델'을 하나의 화면에 통합하였습니다.
- 슬라이더를 조작하면, 가상 실험 애니메이션이 실행됨과 동시에 AI가 4가지 완충재에 대한 파손 확률을 즉시 예측합니다.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
from sklearn.ensemble import RandomForestClassifier
import warnings

# Sklearn 경고 메시지 숨김
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. AI 데이터 셋 생성 및 모델 학습 (백그라운드)
# ==========================================
print("로딩 중: 역학 데이터를 기반으로 AI 모델을 학습시키는 중입니다...")
np.random.seed(42)
num_samples = 2000

# 슬라이더 범위를 커버하는 학습 데이터 생성
masses = np.random.uniform(0.1, 0.6, num_samples)
drop_heights = np.random.uniform(0.1, 3.0, num_samples)
packagings = np.random.randint(0, 4, num_samples)

# 재질 특성: 0=맨바닥, 1=스티로폼, 2=에어캡, 3=종이트레이
pack_props = {
    0: (0.34, 0.005), 
    1: (0.30, 0.012), 
    2: (0.45, 0.025), 
    3: (0.18, 0.020)
}
g = 9.81
is_damaged = []

# 역학 공식을 통해 손상 여부 라벨링
for m, h, p in zip(masses, drop_heights, packagings):
    e, dt = pack_props[p]
    force = m * (np.sqrt(2 * g * h) * (1 + e)) / dt
    bruise_threshold = np.random.normal(150.0, 15.0) # 150N 기준 생물학적 노이즈
    is_damaged.append(1 if force > bruise_threshold else 0)

df = pd.DataFrame({'Mass_kg': masses, 'Drop_Height_m': drop_heights, 'Packaging_Type': packagings, 'Is_Damaged': is_damaged})
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(df[['Mass_kg', 'Drop_Height_m', 'Packaging_Type']], df['Is_Damaged'])
print("✅ AI 모델 학습 완료! 통합 시뮬레이터 창을 띄웁니다.")

# ==========================================
# 2. 물리 시뮬레이션 환경 설정
# ==========================================
init_mass = 0.25
init_drop_height = 1.0
init_thresh = 150.0

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

# ==========================================
# 3. 통합 GUI 화면 구성
# ==========================================
fig = plt.figure(figsize=(16, 7))
fig.subplots_adjust(bottom=0.25, wspace=0.3)
fig.suptitle('[Step 2 + 3 통합] 역학 시뮬레이션 & AI 파손 예측기', fontsize=18, fontweight='bold')

# [차트 1] 물리 낙하 애니메이션
ax_anim = plt.subplot(1, 4, 1)
ax_anim.set_xlim(-0.5, 3.5)
ax_anim.set_ylim(-0.15, 2.5)
ax_anim.set_xticks([0, 1, 2, 3])
ax_anim.set_xticklabels(['맨바닥', '스티로폼', '에어캡', '종이트레이'], fontsize=11)
ax_anim.set_title('물리 낙하 실험 궤적', fontsize=14)
ax_anim.set_ylabel('높이 (m)')
ax_anim.grid(True, linestyle='--', alpha=0.6)
ax_anim.axhline(0, color='black', linewidth=3)

# 바닥 색상 시각화
ax_anim.axhline(-0.05, xmin=0.32, xmax=0.43, color='orange', linewidth=10, alpha=0.5) 
ax_anim.axhline(-0.05, xmin=0.57, xmax=0.68, color='blue', linewidth=10, alpha=0.3) 
ax_anim.axhline(-0.05, xmin=0.82, xmax=0.93, color='green', linewidth=10, alpha=0.5) 

apple_h, = ax_anim.plot([], [], 'ro', markersize=15)
apple_e, = ax_anim.plot([], [], color='orange', marker='o', markersize=15, linestyle='None')
apple_b, = ax_anim.plot([], [], 'bo', markersize=15)
apple_t, = ax_anim.plot([], [], 'go', markersize=15)

# [차트 2] 뉴턴 제2법칙 기반 시간에 따른 충격력 (넓게 표시)
ax_force = plt.subplot(1, 4, (2, 3))
ax_force.set_xlim(0, t_total)
ax_force.set_ylim(0, 900)
ax_force.set_title('물리 역학적 충격력 (Newton)', fontsize=14)
ax_force.set_xlabel('시간 (s)')
ax_force.set_ylabel('충격력 (N)')
ax_force.grid(True, linestyle='--', alpha=0.6)
ax_force.axhline(init_thresh, color='red', linestyle='--', linewidth=2, label='위험(150N)')

line_f_h, = ax_force.plot([], [], 'r-', lw=2, label='맨바닥')
line_f_e, = ax_force.plot([], [], color='orange', lw=2, label='스티로폼')
line_f_b, = ax_force.plot([], [], 'b-', lw=2, label='에어캡')
line_f_t, = ax_force.plot([], [], 'g-', lw=2, label='트레이')
ax_force.legend(loc='upper right', fontsize=9)

# [차트 3] AI 파손 확률 바 차트
ax_ai = plt.subplot(1, 4, 4)
ax_ai.set_ylim(0, 100)
ax_ai.set_title('AI 학습 기반 실시간 손상 확률', fontsize=14)
ax_ai.set_ylabel('손상 확률 (%)')
ax_ai.grid(True, axis='y', linestyle='--', alpha=0.6)
ax_ai.axhline(50, color='red', linestyle='--', linewidth=2, label='위험 기준선(50%)')
bars = ax_ai.bar(['맨바닥', '스티로폼', '에어캡', '트레이'], [0, 0, 0, 0], color=['red', 'orange', 'blue', 'green'], alpha=0.8)
ax_ai.legend(loc='upper right', fontsize=9)

# 슬라이더 UI 구성
axcolor = 'lightgray'
ax_mass = plt.axes([0.15, 0.12, 0.65, 0.03], facecolor=axcolor)
ax_height = plt.axes([0.15, 0.06, 0.65, 0.03], facecolor=axcolor)
s_mass = Slider(ax_mass, '사과 질량 (kg)', 0.1, 0.6, valinit=init_mass, valstep=0.01)
s_height = Slider(ax_height, '낙하 높이 (m)', 0.1, 2.5, valinit=init_drop_height, valstep=0.1)

btn_ax = plt.axes([0.85, 0.06, 0.08, 0.09])
btn_restart = Button(btn_ax, '애니메이션\n재생', hovercolor='white')

current_frame = [0]
global_data = {}

def update_sim(val=None):
    m = s_mass.val
    h = s_height.val
    
    # 충격 발생 순간으로 그래프 동적 확대 (Zoom-in)
    t_fall = np.sqrt(2 * h / g)
    ax_force.set_xlim(max(0, t_fall - 0.05), t_fall + 0.10)
    
    # 1. 역학 계산 (차트 1, 2 업데이트용)
    y_h, f_h, _ = calc_traj(m, h, pack_props[0][0], pack_props[0][1])
    y_e, f_e, _ = calc_traj(m, h, pack_props[1][0], pack_props[1][1])
    y_b, f_b, _ = calc_traj(m, h, pack_props[2][0], pack_props[2][1])
    y_t, f_t, _ = calc_traj(m, h, pack_props[3][0], pack_props[3][1])
    
    global_data['y'] = [y_h, y_e, y_b, y_t]
    global_data['f'] = [f_h, f_e, f_b, f_t]
    
    # 2. AI 예측 (차트 3 업데이트용)
    probs = []
    for p in range(4): # 0~3 포장재 순서대로 예측
        probs.append(model.predict_proba([[m, h, p]])[0][1] * 100)
    
    for bar, prob in zip(bars, probs):
        bar.set_height(prob)
        # 확률이 높으면 빨간색, 중간이면 주황색, 낮으면 초록색
        if prob > 50:
            bar.set_color('red')
        elif prob > 20:
            bar.set_color('orange')
        else:
            bar.set_color('green')
            
    # 시뮬레이션 프레임 초기화
    current_frame[0] = 0

s_mass.on_changed(update_sim)
s_height.on_changed(update_sim)
btn_restart.on_clicked(lambda e: current_frame.__setitem__(0, 0))

# 초기 1회 실행
update_sim()

def frame_generator():
    while True:
        yield current_frame[0]
        if current_frame[0] < num_frames - 1:
            current_frame[0] += 1

def update_anim(f):
    apple_h.set_data([0], [global_data['y'][0][f]])
    apple_e.set_data([1], [global_data['y'][1][f]])
    apple_b.set_data([2], [global_data['y'][2][f]])
    apple_t.set_data([3], [global_data['y'][3][f]])
    
    line_f_h.set_data(time_array[:f+1], global_data['f'][0][:f+1])
    line_f_e.set_data(time_array[:f+1], global_data['f'][1][:f+1])
    line_f_b.set_data(time_array[:f+1], global_data['f'][2][:f+1])
    line_f_t.set_data(time_array[:f+1], global_data['f'][3][:f+1])
    
    return apple_h, apple_e, apple_b, apple_t, line_f_h, line_f_e, line_f_b, line_f_t

ani = animation.FuncAnimation(fig, update_anim, frames=frame_generator, interval=1000/fps, blit=False, cache_frame_data=False)
plt.show()
