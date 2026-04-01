"""
Step 6: Power Law Model Curve Fitting - 토마토 케첩 데이터 적용 (Advanced 과제)
이 스크립트는 원본 step1의 코드를 토마토 케첩 데이터에 적용한 버전입니다.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from scipy.optimize import curve_fit

# 1. 대상 유체 데이터 보간 (토마토 케첩)
# 전단 속도 (Shear Rate, 1/s): 5 ~ 100
shear_rate_data = np.array([5, 10, 20, 50, 100])
# 전단 응력 (Shear Stress, Pa)
shear_stress_data = np.array([32.0, 40.5, 52.1, 70.8, 89.2])

# 2. 파워 로우(Power Law) 모델 함수 정의
# 식: \tau = K * \dot{\gamma}^n
def power_law(gamma, K, n):
    return K * (gamma ** n)

# 3. 최적 계수 찾기 (Curve Fitting)
popt, pcov = curve_fit(power_law, shear_rate_data, shear_stress_data)

K_est, n_est = popt
print(f"--- Power Law 피팅 결과 (토마토 케첩) ---")
print(f"농도 계수 (K): {K_est:.4f} Pa·s^n")
print(f"유동 지수 (n): {n_est:.4f}")

# 4. 결괏값 도식화 및 그래프 모델
shear_rate_smooth = np.linspace(0, 100, 200)
shear_stress_fit = power_law(shear_rate_smooth, K_est, n_est)

plt.figure(figsize=(8, 6))

# 실험 데이터 산점도 (Scatter)
plt.scatter(shear_rate_data, shear_stress_data, color='red', label='Experimental Data (Tomato Ketchup)', s=50, zorder=3)

# 피팅된 파워 로우 곡선 (Line)
plt.plot(shear_rate_smooth, shear_stress_fit, color='blue', linewidth=2, label=rf'Power Law Fit ($\tau = {K_est:.2f} \cdot \dot{{\gamma}}^{{{n_est:.2f}}}$)', zorder=2)

plt.title('Non-Newtonian Fluid: Power Law Curve Fitting (Tomato Ketchup)', fontsize=14, fontweight='bold')
plt.xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
plt.ylabel('Shear Stress ($\\tau$, Pa)', fontsize=12)
plt.xlim(0, 110)
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=11)

plt.tight_layout()
plt.show()
