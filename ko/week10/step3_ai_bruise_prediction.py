"""
10주차 실습 Step 3: 농작물 손상 예측 AI 모델 (Physics-Informed Machine Learning)
- 물리 시뮬레이션을 통해 2,000개의 가상 충격 데이터를 생성합니다.
- 머신러닝(Random Forest)을 사용하여 질량, 낙하 높이, 포장재 종류만으로 멍(Bruise) 발생 여부를 예측하는 AI를 만듭니다.
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("="*60)
print("[1단계] 물리 역학 기반 가상 농작물(사과) 충격 데이터 생성 중...")
print("="*60)

# 1. 데이터 시뮬레이션 (물리 공식 기반)
np.random.seed(42)
num_samples = 2000

# 랜덤 Feature 생성 (농작물의 개체 차이 및 다양한 사고 상황 가정)
masses = np.random.normal(0.25, 0.03, num_samples)  # 질량: 0.25kg 평균, 정규분포
drop_heights = np.random.uniform(0.3, 1.5, num_samples)  # 낙하 높이: 0.3m ~ 1.5m, 균등분포
# 포장재: 0=맨바닥, 1=스티로폼, 2=에어캡, 3=종이트레이
packagings = np.random.randint(0, 4, num_samples)

# 재질별 특성 딕셔너리 (반발계수 e, 충돌시간 dt)
pack_props = {
    0: (0.34, 0.005),  # 맨바닥
    1: (0.30, 0.012),  # 스티로폼
    2: (0.45, 0.025),  # 에어캡
    3: (0.18, 0.020)   # 종이트레이
}

g = 9.81
is_damaged = []
max_forces = []

for m, h, p in zip(masses, drop_heights, packagings):
    e, dt = pack_props[p]
    
    # 물리 공식 적용: 충돌 직전 속도 및 직후 속도
    v1 = np.sqrt(2 * g * h)
    v2 = v1 * e
    
    # 최대 충격력 계산 F = m * (v1 + v2) / dt
    force = m * (v1 + v2) / dt
    max_forces.append(force)
    
    # 생물학적 한계치 (과일마다 단단함의 개체 차이가 있다고 가정, 150N 기준 정규분포 노이즈)
    bruise_threshold = np.random.normal(150.0, 15.0)
    
    if force > bruise_threshold:
        is_damaged.append(1) # 손상됨(Bruised)
    else:
        is_damaged.append(0) # 안전함(Safe)

# DataFrame 생성
df = pd.DataFrame({
    'Mass_kg': masses,
    'Drop_Height_m': drop_heights,
    'Packaging_Type': packagings,
    'Is_Damaged': is_damaged
})

print(f"총 {num_samples}개의 데이터가 성공적으로 생성되었습니다.\n")
print(df.head())
print("\n손상 데이터 비율:")
print(df['Is_Damaged'].value_counts(normalize=True).apply(lambda x: f"{x*100:.1f}%"))

# 2. AI 모델 학습
print("\n" + "="*60)
print("[2단계] AI 모델(Random Forest) 학습 진행 중...")
print("="*60)
X = df[['Mass_kg', 'Drop_Height_m', 'Packaging_Type']]
y = df['Is_Damaged']

# 학습용 데이터와 테스트용 데이터 분할 (8:2 비율)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 랜덤 포레스트 분류기 생성 및 학습
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 3. 모델 평가
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\n[모델 평가 결과]")
print(f"[AI 예측 정확도(Accuracy)]: {acc * 100:.2f}%\n")
print(classification_report(y_test, y_pred, target_names=['안전(0)', '손상(1)']))

# 4. 피처 중요도(Feature Importance) 시각화
importance = model.feature_importances_
features = ['과일 질량 (Mass)', '낙하 높이 (Height)', '포장재 종류 (Packaging)']

plt.figure(figsize=(8, 5))
sns.barplot(x=importance, y=features, palette='viridis', hue=features, legend=False)
plt.title('농작물 손상 예측 AI - Feature Importance (변수 중요도)', fontsize=14, fontweight='bold')
plt.xlabel('중요도 (기여도 비율)', fontsize=12)
plt.ylabel('입력 변수', fontsize=12)
plt.tight_layout()

os.makedirs('ko/week10/images', exist_ok=True)
plt.savefig('ko/week10/images/ai_feature_importance.png', dpi=300)
print("\n[Feature Importance 그래프가 'ko/week10/images/ai_feature_importance.png'에 저장되었습니다.]")
# plt.show() # 서버/백그라운드 실행을 위해 팝업은 끔

# 5. 새로운 가상 상황에 대한 AI의 예측 (Inference)
print("\n" + "="*60)
print("[3단계] 학습된 AI 모델을 활용한 새로운 가상 상황 예측 테스트")
print("="*60)

import warnings
warnings.filterwarnings('ignore', category=UserWarning) # 스킷런 경고 무시

test_cases = [
    [0.30, 1.2, 0], # 300g 사과, 1.2m 높이, 맨바닥
    [0.30, 1.2, 3], # 300g 사과, 1.2m 높이, 종이트레이
    [0.20, 0.8, 1], # 200g 사과, 0.8m 높이, 스티로폼
    [0.25, 0.5, 2], # 250g 사과, 0.5m 높이, 에어캡
]

pack_names = {0: "맨바닥", 1: "스티로폼", 2: "에어캡", 3: "종이트레이"}

for case in test_cases:
    mass, height, pack = case
    pred = model.predict([case])[0]
    prob = model.predict_proba([case])[0][1] # 손상 확률
    
    result = "[손상 위험 (Bruised)]" if pred == 1 else "[안전 예상 (Safe)]"
    print(f"- {mass:.2f}kg 사과를 {height:.1f}m에서 [{pack_names[pack]}]에 떨어뜨릴 때")
    print(f"   => AI 판정: {result} (AI가 계산한 손상 확률: {prob*100:.1f}%)")
    print("-" * 50)
