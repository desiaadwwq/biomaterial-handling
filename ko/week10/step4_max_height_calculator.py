"""
10주차 실습 Step 4: 완충재별 최대 허용 낙하 높이 자동 산출 도구
- 주어진 과일 질량과 손상 임계치를 바탕으로,
- 각 포장재(맨바닥, 스티로폼, 에어캡, 종이트레이)에서 멍이 들지 않는 최대 낙하 높이를 계산합니다.
- 계산된 결과를 Excel(.xlsx) 파일로 내보냅니다.
"""

import pandas as pd
import numpy as np

# 1. 초기 파라미터 설정
g = 9.81
mass = 0.25           # 과일 질량 (kg)
f_limit = 150.0       # 멍 발생 임계치 (N)

# 재질별 특성 (반발계수 e, 충돌시간 dt)
materials = {
    "맨바닥": {"e": 0.34, "dt": 0.005},
    "발포 스티로폼": {"e": 0.30, "dt": 0.012},
    "에어캡": {"e": 0.45, "dt": 0.025},
    "종이 트레이": {"e": 0.18, "dt": 0.020}
}

print("=" * 60)
print(f"[최대 허용 낙하 높이 산출 시뮬레이터]")
print(f"   - 과일 질량: {mass} kg")
print(f"   - 손상 임계치: {f_limit} N")
print("=" * 60)

# 2. 최대 높이 계산 함수
# F = m * sqrt(2gh) * (1+e) / dt
# sqrt(2gh) = (F * dt) / (m * (1+e))
# h = [ (F * dt) / (m * (1+e)) ]^2 / (2g)
def calculate_max_height(m, f_th, e, dt):
    v_impact_limit = (f_th * dt) / (m * (1 + e))
    h_max = (v_impact_limit ** 2) / (2 * g)
    return h_max

# 3. 각 재질별 결과 계산
results = []
for name, props in materials.items():
    e = props["e"]
    dt = props["dt"]
    h_max = calculate_max_height(mass, f_limit, e, dt)
    
    # 1.0m에서 떨어뜨렸을 때의 실제 충격력도 참고용으로 계산
    v_1m = np.sqrt(2 * g * 1.0)
    force_1m = mass * v_1m * (1 + e) / dt
    
    results.append({
        "포장재 종류": name,
        "반발 계수 (e)": e,
        "충돌 시간 (dt, s)": dt,
        "1.0m 낙하 시 충격력 (N)": round(force_1m, 1),
        "최대 허용 낙하 높이 (m)": round(h_max, 3)
    })
    
    print(f"▶ {name}")
    print(f"   - 1.0m 낙하 시 충격력: {force_1m:.1f} N")
    print(f"   - [손상 없는 최대 낙하 높이]: {h_max:.3f} m")

# 4. DataFrame 생성 및 Excel 내보내기
df = pd.DataFrame(results)

# 결과를 Excel 파일로 저장
output_path = "ko/week10/최대_허용_낙하높이_결과.xlsx"
df.to_excel(output_path, index=False)

print("=" * 60)
print(f"[계산 결과가 엑셀 파일로 자동 저장되었습니다]: {output_path}")
print("=" * 60)
