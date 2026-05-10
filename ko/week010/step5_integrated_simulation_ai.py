"""
10주차 실습 Step 5 (Master): 통합 시뮬레이터 (물리 역학 + 머신러닝 AI)
- 낙하 시뮬레이션 애니메이션
- 위치-시간 그래프 (추가됨)
- 가속도-시간 그래프 (추가됨)
- 충격력-시간 그래프 (동적 줌인)
- AI 파손 확률 예측 바 차트
위 5가지 요소를 하나의 대시보드에 통합 구현하였습니다.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
from sklearn.ensemble import RandomForestClassifier
import warnings
import matplotlib.gridspec as gridspec

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

masses = np.random.uniform(0.1, 0.6, num_samples)
drop_heights = np.random.uniform(0.1, 3.0, num_samples)
packagings = np.random.randint(0, 4, num_samples)

pack_props = {
    0: (0.34, 0.005), 
    1: (0.30, 0.012), 
    2: (0.45, 0.025), 
    3: (0.18, 0.020)
}
g = 9.81
is_damaged = []

for m, h, p in zip(masses, drop_heights, packagings):
    e, dt = pack_props[p]
    force = m * (np.sqrt(2 * g * h) * (1 + e)) / dt
    bruise_threshold = np.random.normal(150.0, 15.0) 
    is_damaged.append(1 if force > bruise_threshold else 0)

df = pd.DataFrame({'Mass_kg': masses, 'Drop_Height_m': drop_heights, 'Packaging_Type': packagings, 'Is_Damaged': is_damaged})
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(df[['Mass_kg', 'Drop_Height_m', 'Packaging_Type']], df['Is_Damaged'])
print("✅ AI 모델 학습 완료! 마스터 시뮬레이터 창을 띄웁니다.")

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
    a = np.zeros(num_frames)
    
    for i, t in enumerate(time_array):
        if t < t_fall:
            y[i] = drop_height - 0.5 * g * t**2
            a[i] = -g
        elif t < t_fall + dt:
            compress = (t - t_fall) / dt
            y[i] = -0.05 * np.sin(compress * np.pi)
            f[i] = force
            a[i] = force / mass - g
        else:
            t_b = t - (t_fall + dt)
            y[i] = v2 * t_b - 0.5 * g * t_b**2
            a[i] = -g
            if y[i] < 0: 
                y[i] = 0
                a[i] = 0
    return y, f, a

# ==========================================
# 3. 마스터 GUI 화면 구성 (2x3 GridSpec)
# ==========================================
fig = plt.figure(figsize=(18, 9))
fig.subplots_adjust(bottom=0.20, top=0.90, left=0.05, right=0.95, wspace=0.3, hspace=0.4)
fig.suptitle('[Step 5 마스터] 물리 낙하 궤적, 가속도 및 AI 파손 예측 대시보드', fontsize=18, fontweight='bold')

gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1])

# [차트 1: 애니메이션] (Top-Left)
ax_anim = fig.add_subplot(gs[0, 0])
ax_anim.set_xlim(-0.5, 3.5)
ax_anim.set_ylim(-0.15, 2.5)
ax_anim.set_xticks([0, 1, 2, 3])
ax_anim.set_xticklabels(['맨바닥', '스티로폼', '에어캡', '트레이'])
ax_anim.set_title('물리 낙하 시뮬레이션', fontsize=13)
ax_anim.set_ylabel('높이 (m)')
ax_anim.grid(True, linestyle='--', alpha=0.6)
ax_anim.axhline(0, color='black', linewidth=3)
ax_anim.axhline(-0.05, xmin=0.32, xmax=0.43, color='orange', linewidth=10, alpha=0.5) 
ax_anim.axhline(-0.05, xmin=0.57, xmax=0.68, color='blue', linewidth=10, alpha=0.3) 
ax_anim.axhline(-0.05, xmin=0.82, xmax=0.93, color='green', linewidth=10, alpha=0.5) 

apple_h, = ax_anim.plot([], [], 'ro', markersize=12)
apple_e, = ax_anim.plot([], [], color='orange', marker='o', markersize=12, linestyle='None')
apple_b, = ax_anim.plot([], [], 'bo', markersize=12)
apple_t, = ax_anim.plot([], [], 'go', markersize=12)

# [차트 2: 위치-시간] (Top-Center)
ax_pos = fig.add_subplot(gs[0, 1])
ax_pos.set_xlim(0, t_total)
ax_pos.set_ylim(-0.1, 2.5)
ax_pos.set_title('위치-시간 (Position-Time)', fontsize=13)
ax_pos.set_ylabel('높이 (m)')
ax_pos.grid(True, linestyle='--', alpha=0.6)
line_p_h, = ax_pos.plot([], [], 'r-', lw=2, label='맨바닥')
line_p_e, = ax_pos.plot([], [], color='orange', lw=2, label='스티로폼')
line_p_b, = ax_pos.plot([], [], 'b-', lw=2, label='에어캡')
line_p_t, = ax_pos.plot([], [], 'g-', lw=2, label='트레이')
ax_pos.legend(loc='upper right', fontsize=8)

# [차트 3: 가속도-시간] (Top-Right)
ax_accel = fig.add_subplot(gs[0, 2])
ax_accel.set_xlim(0, t_total)
ax_accel.set_ylim(-20, 4000)
ax_accel.set_title('가속도-시간 (Acceleration-Time)', fontsize=13)
ax_accel.set_ylabel('가속도 (m/s²)')
ax_accel.grid(True, linestyle='--', alpha=0.6)
line_a_h, = ax_accel.plot([], [], 'r-', lw=2, label='맨바닥')
line_a_e, = ax_accel.plot([], [], color='orange', lw=2, label='스티로폼')
line_a_b, = ax_accel.plot([], [], 'b-', lw=2, label='에어캡')
line_a_t, = ax_accel.plot([], [], 'g-', lw=2, label='트레이')

# [차트 4: AI 예측] (Bottom-Left)
ax_ai = fig.add_subplot(gs[1, 0])
ax_ai.set_ylim(0, 100)
ax_ai.set_title('AI 학습 기반 실시간 손상 확률 예측', fontsize=13)
ax_ai.set_ylabel('손상 확률 (%)')
ax_ai.grid(True, axis='y', linestyle='--', alpha=0.6)
ax_ai.axhline(50, color='red', linestyle='--', linewidth=2, label='위험(50%)')
bars = ax_ai.bar(['맨바닥', '스티로폼', '에어캡', '트레이'], [0, 0, 0, 0], color=['red', 'orange', 'blue', 'green'], alpha=0.8)

# [차트 5: 충격력-시간 확대] (Bottom-Center & Right)
ax_force = fig.add_subplot(gs[1, 1:])
ax_force.set_ylim(0, 900)
ax_force.set_title('물리 충격력 (Newton) - 임팩트 순간 동적 확대(Zoom)', fontsize=13)
ax_force.set_xlabel('시간 (s)')
ax_force.set_ylabel('충격력 (N)')
ax_force.grid(True, linestyle='--', alpha=0.6)
ax_force.axhline(init_thresh, color='red', linestyle='--', linewidth=2, label='위험(150N)')
line_f_h, = ax_force.plot([], [], 'r-', lw=2, label='맨바닥')
line_f_e, = ax_force.plot([], [], color='orange', lw=2, label='스티로폼')
line_f_b, = ax_force.plot([], [], 'b-', lw=2, label='에어캡')
line_f_t, = ax_force.plot([], [], 'g-', lw=2, label='트레이')
ax_force.legend(loc='upper right', fontsize=9)

# 슬라이더 UI
axcolor = 'lightgray'
ax_mass = plt.axes([0.15, 0.08, 0.65, 0.03], facecolor=axcolor)
ax_height = plt.axes([0.15, 0.03, 0.65, 0.03], facecolor=axcolor)
s_mass = Slider(ax_mass, '사과 질량 (kg)', 0.1, 0.6, valinit=init_mass, valstep=0.01)
s_height = Slider(ax_height, '낙하 높이 (m)', 0.1, 2.5, valinit=init_drop_height, valstep=0.1)

btn_ax = plt.axes([0.85, 0.03, 0.08, 0.08])
btn_restart = Button(btn_ax, '애니메이션\n재생', hovercolor='white')

current_frame = [0]
global_data = {}

def update_sim(val=None):
    m = s_mass.val
    h = s_height.val
    
    # 임팩트 줌인
    t_fall = np.sqrt(2 * h / g)
    ax_force.set_xlim(max(0, t_fall - 0.05), t_fall + 0.10)
    
    # 가속도 Y축 동적 스케일링 (최대 가속도에 맞춤)
    y_h, f_h, a_h = calc_traj(m, h, pack_props[0][0], pack_props[0][1])
    y_e, f_e, a_e = calc_traj(m, h, pack_props[1][0], pack_props[1][1])
    y_b, f_b, a_b = calc_traj(m, h, pack_props[2][0], pack_props[2][1])
    y_t, f_t, a_t = calc_traj(m, h, pack_props[3][0], pack_props[3][1])
    
    max_a = max(np.max(a_h), np.max(a_e), np.max(a_b), np.max(a_t))
    ax_accel.set_ylim(-20, max_a * 1.1)
    
    global_data['y'] = [y_h, y_e, y_b, y_t]
    global_data['f'] = [f_h, f_e, f_b, f_t]
    global_data['a'] = [a_h, a_e, a_b, a_t]
    
    # AI 예측
    probs = []
    for p in range(4):
        probs.append(model.predict_proba([[m, h, p]])[0][1] * 100)
    
    for bar, prob in zip(bars, probs):
        bar.set_height(prob)
        if prob > 50: bar.set_color('red')
        elif prob > 20: bar.set_color('orange')
        else: bar.set_color('green')
            
    current_frame[0] = 0

s_mass.on_changed(update_sim)
s_height.on_changed(update_sim)
btn_restart.on_clicked(lambda e: current_frame.__setitem__(0, 0))

update_sim()

def frame_generator():
    while True:
        yield current_frame[0]
        if current_frame[0] < num_frames - 1:
            current_frame[0] += 1

def update_anim(f):
    # 애니메이션
    apple_h.set_data([0], [global_data['y'][0][f]])
    apple_e.set_data([1], [global_data['y'][1][f]])
    apple_b.set_data([2], [global_data['y'][2][f]])
    apple_t.set_data([3], [global_data['y'][3][f]])
    
    # 위치-시간 (전체 범위 중 f까지만)
    line_p_h.set_data(time_array[:f+1], global_data['y'][0][:f+1])
    line_p_e.set_data(time_array[:f+1], global_data['y'][1][:f+1])
    line_p_b.set_data(time_array[:f+1], global_data['y'][2][:f+1])
    line_p_t.set_data(time_array[:f+1], global_data['y'][3][:f+1])
    
    # 가속도-시간 (전체 범위 중 f까지만)
    line_a_h.set_data(time_array[:f+1], global_data['a'][0][:f+1])
    line_a_e.set_data(time_array[:f+1], global_data['a'][1][:f+1])
    line_a_b.set_data(time_array[:f+1], global_data['a'][2][:f+1])
    line_a_t.set_data(time_array[:f+1], global_data['a'][3][:f+1])
    
    # 충격력-시간 (동적 줌인)
    line_f_h.set_data(time_array[:f+1], global_data['f'][0][:f+1])
    line_f_e.set_data(time_array[:f+1], global_data['f'][1][:f+1])
    line_f_b.set_data(time_array[:f+1], global_data['f'][2][:f+1])
    line_f_t.set_data(time_array[:f+1], global_data['f'][3][:f+1])
    
    return apple_h, apple_e, apple_b, apple_t, line_p_h, line_p_e, line_p_b, line_p_t, line_a_h, line_a_e, line_a_b, line_a_t, line_f_h, line_f_e, line_f_b, line_f_t

ani = animation.FuncAnimation(fig, update_anim, frames=frame_generator, interval=1000/fps, blit=False, cache_frame_data=False)
plt.show()
