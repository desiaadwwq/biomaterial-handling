import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. 데이터 준비 (전분 풀)
shear_rate = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
shear_stress = np.array([18.5, 29.3, 38.5, 46.8, 54.3, 61.2, 67.8, 74.0, 80.0, 85.8])

# 2. 기존 비선형 curve_fit 수행
def power_law(gamma, K, n):
    return K * (gamma ** n)

popt, _ = curve_fit(power_law, shear_rate, shear_stress)
K_curve, n_curve = popt

# 3. 로그-로그 스케일 변환 및 1차 선형 회귀 (polyfit)
log_gamma = np.log10(shear_rate)
log_tau = np.log10(shear_stress)

# 1차 회귀: log(tau) = n * log(gamma) + log(K)
n_poly, log_K_poly = np.polyfit(log_gamma, log_tau, 1)
K_poly = 10 ** log_K_poly

# 4. 결과 출력
print("--- [Advanced 1] 결과 비교 ---")
print(f"Curve Fit 결과: K = {K_curve:.4f}, n = {n_curve:.4f}")
print(f"Polyfit 결과  : K = {K_poly:.4f}, n = {n_poly:.4f}")

# 5. 시각화 (로그 선형화 차트)
plt.figure(figsize=(8, 6))
plt.scatter(log_gamma, log_tau, color='blue', label='Log Data', zorder=3)
x_line = np.linspace(min(log_gamma), max(log_gamma), 100)
y_line = n_poly * x_line + log_K_poly
plt.plot(x_line, y_line, color='red', label=rf'Linear Fit ($n={n_poly:.3f}$)', lw=2)

plt.title('[Advanced] Log-Log Scale Linearization')
plt.xlabel('log(Shear Rate)')
plt.ylabel('log(Shear Stress)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
