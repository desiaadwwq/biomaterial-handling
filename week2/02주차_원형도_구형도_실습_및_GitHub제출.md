# 🍏 2주차: 디지털 이미지 프로세싱 기반 형상 분석 실습
**- OpenCV 원형도 및 구형도 산출 알고리즘 고찰 및 GitHub 제출 가이드 -**

---

## 0. 실습 준비 공통 가이드 (환경 설정 및 코드 실행)

본 실습은 파이썬과 외부 라이브러리(OpenCV, Numpy) 구동을 전제로 합니다. 개인 PC에서 실습을 진행하기 위해 아래 단계를 가장 먼저 수행하세요.

### 0-1. 교수/조교 제공 실습 베이스코드 및 데이터 다운로드
학생들은 매주 배포되는 실습 베이스 코드와 영상 데이터(예: [`apple_side_A.png`](apple_side_A.png))를 자신의 로컬 PC로 가져와야 합니다.
1. 조교(또는 교수님)가 제공한 실습용 GitHub 저장소 주소로 이동하거나, 최상위 [**`README.md`**](../README.md) 안내를 따릅니다.
2. 터미널(또는 명령 프롬프트)에서 해당 저장소를 통째로 다운로드(Clone)합니다.
   ```bash
   git clone [제공된_실습_레포지토리_주소.git]
   ```
   *Git 사용이 익숙지 않은 경우, GitHub 웹사이트의 `Code` 버튼 > `Download ZIP`을 통해 압축 해제하여 활용해도 무방합니다. 혹은 AI에게 Git명령이나 방법을 물어도 됩니다.* 

### 0-2. IDE (통합 개발 환경) 실행
다운로드 또는 압축 해제한 해당 **실습 주차 폴더(예: `week2`)를 직접 지정하여 열어야 합니다.**
1. VS Code, Cursor, Antigravity 등 본인에게 익숙한 IDE를 실행합니다.
2. 상단 메뉴의 `File` > `Open Folder...` (폴더 열기)를 선택하여 실습 파일들이 위치한 폴더를 엽니다.

### 0-3. 파이썬 라이브러리 설치 및 실행 확인
1. IDE 내부 터미널(VS Code의 경우 `Ctrl + \``)을 엽니다. 명령어 입력 창의 경로가 실습 폴더인지 반드시 확인합니다.
2. OpenCV 처리에 필요한 필수 라이브러리를 설치합니다.
   ```bash
   pip install opencv-python numpy
   ```
3. 코드가 동작하는지 확인하기 위해 제공된 스크립트를 파이썬으로 직접 실행해 봅니다.
   ```bash
   python test_script.py (또는 본인이 생성할 파일명)
   ```

*(이제 아래 이론 및 단계별 튜토리얼을 따라 실제 형상 분석 코드를 작성해 봅시다!)*

---

## 1. 기하학적 형상 지표: 원형도와 구형도의 정의와 차이

학술적으로 '원형도'와 '구형도'는 혼용되기도 하나, 기하학적 관점에서는 측정 목적이 다름.

### 1-1. 원형도 (Circularity)
- **정의**: '형상 계수(Form Factor)' 또는 '등주 비(Isoperimetric Quotient)'라 불림
- **측정 목적**: 객체의 전체적인 형태가 "원(Circle)"에 얼마나 가까운지 평가
- **수식**: `Circularity = (4 × π × Area) / Perimeter²`
- **특징**:
  - 완벽한 원일 때 값 1.0 (최대치) 산출
  - 형상이 찌그러지거나 경계가 복잡할수록 0에 수렴
  - 둘레 길이에 의존하므로 윤곽선 노이즈 및 거칠기(Roughness)에 매우 민감함

### 1-2. 구형도 (Sphericity) & 라운드니스 (Roundness)
- **와델(Wadell) 구형도**: 
  - 3차원 입자 부피와 동일 체적 구의 표면적 비
  - 2차원 투영에서는 **면적 대 외접원 면적 비**로 간접 산출 혹은 객체의 회전된 Bounding Box 가로세로 치수 비율 활용
- **라운드니스**:
  - 모서리 부드러움 측정 (평균 곡률 반경 / 최대 내접원 반경)
  - 입자 신장도(Elongation)와 무관하게 모서리 마모도 수치화

### [요약 표]
| 지표명 | 수식 또는 핵심 파라미터 | 주요 측정 대상 | 민감 요소 |
| --- | --- | --- | --- |
| **원형도 (Circularity)** | `(4π × Area) / 둘레²` | 전체적인 원형 근접도 | 노이즈, 형태 불규칙성 |
| **구형도 (Sphericity)** | 기하평균직경 / L 등 | 표면적/체적 비 (3D 근접도) | 신장도 (Elongation) |
| **라운드니스** | 모서리 곡률반경 등 | 모서리 매끄러움 | 굴곡, 마모도 |

---

## 2. 디지털 이미지 프로세싱 단계별 형상 분석 알고리즘

### 단계 1: 영상 획득 및 Grayscale 변환
- BGR(RGB) 채널 연산량을 줄이고 휘도 정보만으로 1차원 연산 수행 위함

### 단계 2: 노이즈 제거 (Gaussian Blur)
- 조명 난반사 및 사과 표면 점/질감 노이즈 평활화
- 윤곽선(둘레) 계산 시 노이즈로 인한 둘레값 과팽창 방지 (원형도 오류 차단)

### 단계 3: 이진화 (Otsu's Thresholding)
- 배경과 전경(사과)을 분리
- 히스토그램 자동 분석을 통한 최적 임계값 도출

### 단계 4: 윤곽선(Contour) 검출 및 필터링
- `cv2.findContours` 로 외곽선 좌표 배열 검출
- 면적(`cv2.contourArea`) 기준 미세 노이즈 객체 필터링

### 단계 5: 기하학적 모멘트 기반 특성 도출
- 면적(Area), 둘레(Perimeter, `cv2.arcLength`) 추출
- 캘리브레이션 마커(Ruler) 적용을 통한 실제 mm 환산 (PPM: Pixels Per Metric) 적용

---

## 3. OpenCV 파이썬 알고리즘 실습 코드 분할 튜토리얼

본 과정은 학생들이 각 단계를 순차적으로 실행하며 결과의 변화를 시각적으로 이해할 수 있도록 **3개의 별도 파이썬 파일**로 분할 구성되었습니다.

### 📝 [필수] 실습 환경 세팅 및 코드 실행 방법
1. **패키지 설치**: 로컬 명령 프롬프트(cmd) 또는 VScode 터미널을 열고 필요한 라이브러리를 설치합니다.
   ```bash
   pip install opencv-python numpy
   ```
2. **코드 파일 생성 또는 열기**: 아래 제시된 3-1, 3-2, 3-3 단계의 코드를 각각 편집기에서 엽니다. (동일 폴더 내에 [`apple_side_A.png`](apple_side_A.png) 이미지 필수)
3. **코드 순차 실행**: 터미널에서 아래 명령어를 한 줄씩 차례대로 입력하여 영상 처리 결과 창이 어떻게 달라지는지 확인합니다. 창에 표시된 이미지는 **아무 키(Enter 등)나 누르면** 닫히고 종료됩니다.
   ```bash
   python step1_preprocess.py
   python step2_contour.py
   python step3_shape_analysis.py
   ```

---

### 3-1. `step1_preprocess.py`: 이미지 로드 및 전처리
이진화 및 윤곽선 검출을 위해 복잡한 컬러 이미지를 회색조(Grayscale)로 바꾸고 미세 노이즈를 흐리게(Blur) 만듭니다.

```python
import cv2
import numpy as np

# 1. 영상 로드 (한글 경로 지원을 위해 imdecode 사용 권장)
image_path = 'apple_side_A.png'
img_array = np.fromfile(image_path, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

if img is None:
    print("Error: 이미지를 찾을 수 없습니다.")
    exit()

original_display = img.copy()

# 2. 전처리 (그레이스케일 및 Gaussian Blur)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 중간 결과 확인 (키 입력 시 다음 창으로)
cv2.imshow("Step 1: Grayscale & Blurred", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 3-2. [`step2_contour.py`](step2_contour.py): 이진화 및 사과 윤곽선 인식
배경과 사과를 분리하고(Otsu), 분리된 흰색 영역의 외곽선(Contour) 좌표 배열을 도출합니다.

```python
import cv2
import numpy as np

# (이전 단계: 로드 및 전처리 수행 생략, 위 코드에서 이어짐 가정)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. 이진화 (배경이 흰색이므로 INV 옵션 사용 + Otsu 자동 임계값)
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 4. 윤곽선 추출
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 5. 윤곽선 시각화 처리
for cnt in contours:
    area = cv2.contourArea(cnt)
    
    # [중요] 미세 노이즈 윤곽선 제거
    if area < 500:
        continue
    
    # 사과 윤곽선을 이미지에 초록색(0, 255, 0) 두께 2로 표시
    cv2.drawContours(original_display, [cnt], -1, (0, 255, 0), 2)

cv2.imshow("Step 2: Threshold & Contour", original_display)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 3-3. [`step3_shape_analysis.py`](step3_shape_analysis.py): 형태 지표(원형도, 구형도) 최종 도출
도출된 윤곽선을 기준으로 면적, 둘레를 연산해 원형도를 구하고, Bounding Box로 구형도를 수학적으로 도출하여 이미지에 표출합니다.

```python
import cv2
import numpy as np
import math

# (이전 1~2 단계 전처리 및 Contour 도출 상태 이어받기)
# ... [contours 도출까지 수행됨] ...

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 500:
        continue
        
    perimeter = cv2.arcLength(cnt, True)
    if perimeter == 0:
        continue
        
    # 6. 형상 지표 계산 로직
    # A. 원형도 (Circularity) 산출 (둘레와 면적의 비율)
    circularity = (4 * math.pi * area) / (perimeter ** 2)
    
    # B. 구형도 (Sphericity) 산출을 위한 Bounding Box 치수
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int32(box) # 화면 표출을 위한 좌표 정수화
    
    dim1, dim2 = rect[1]
    pixel_L = max(dim1, dim2)
    pixel_W = min(dim1, dim2)
    
    # (실습 가정: 정상 사과 상면 픽셀 T가 304.1로 사전 측정됨)
    pixel_T = 304.1
    GMD = (pixel_L * pixel_W * pixel_T) ** (1/3)
    sphericity = (GMD / pixel_L) * 100
    
    # 7. 시각화 처리
    # 타겟 사과 초록색 윤곽선 표시 및 Bounding Box 파란색 표시
    cv2.drawContours(original_display, [cnt], -1, (0, 255, 0), 2)
    cv2.drawContours(original_display, [box], 0, (255, 0, 0), 2)
    
    # 객체의 기하학적 중심점(Centroid) 도출을 위한 OpenCV 모멘트 연산
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        
        # 중심점 부근에 결과값 텍스트 표출
        cv2.putText(original_display, f"Circularity: {circularity:.3f}", (cx - 60, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(original_display, f"Sphericity: {sphericity:.1f}%", (cx - 60, cy + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# 8. 최종 결과물 GUI 출력
cv2.imshow("Step 3: Final Shape Analysis", original_display)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### [실습 고찰 포인트: 디지털 격자 한계 (Aliasing)]
- 디지털 이미지 특성상 사선의 둥근 경계가 계단형 격자(Grid)로 인식됨
- 실제보다 둘레 픽셀이 항상 길게 측정되는 '계단 현상(Aliasing)' 수반
- 완벽한 구형 객체라도 원형도가 `1.0`이 아닌 `0.85 ~ 0.9` 내외로 산출될 수 있음을 고찰 요망

---

## 4. 실습 결과물 버전 관리 및 GitHub 제출 가이드 (주석 기반 폴더 관리)

학생들은 매주 새로운 저장소(Repository)를 만들 필요 없이, **하나의 마스터 저장소(예: `biomaterial-handling`) 내에 주차별(week02, week03...) 폴더를 생성하여 과제를 누적 관리**해야 합니다.

### 4-1. 프로젝트 Git 저장소 초기화 (최초 1회만 수행)
내 컴퓨터의 학습용 최상위 폴더(예: `C:\biomaterial-handling`) 내에서 명령 프롬프트(또는 터미널)를 엽니다.
1. `git init` : 현재 최상위 폴더를 로컬 Git 저장소로 초기화합니다.
2. (GitHub 웹사이트) `biomaterial-handling` 이름으로 새 Repository를 생성합니다.
3. `git remote add origin https://github.com/[본인아이디]/biomaterial-handling.git` : 원격 저장소 주소를 연동합니다.

### 4-2. 주차별(Week) 과제 폴더 생성 및 소스코드 저장
매주 새로운 실습이 주어질 때마다 최상위 폴더 내에 해당 주차의 폴더를 만들고 그 안에 코드를 저장합니다.
1. 이번 주 과제 폴더 생성: `week02` (다음 주는 `week03`)
2. `week02` 폴더 내에 방금 작성한 파이썬 스크립트(`step1`, `step2`, `step3`), 원본 이미지(`apple_side_A.png`), 그리고 결과 창 캡처 이미지를 모두 복사/저장합니다.

### 4-3. GitHub 원격 저장소로 과제 Push (매주 수행)
폴더 정리가 끝났다면 최상위 경로 터미널에서 아래 명령을 통해 추가된 주차별 코드만 깃허브에 올립니다.
1. `git add .` : 변경되거나 새롭게 추가된 주차별 폴더(week02 등) 전체를 스테이징(Staging)
2. `git commit -m "Add week02 shape analysis python scripts"` : 2주차 스냅샷 저장
3. `git push -u origin main` : (최초 시에만 `-u origin main` 사용, 이후엔 `git push`만 입력)
   - **주의**: 비밀번호 대신 **개인 액세스 토큰 (PAT, Personal Access Token)** 사용을 권장합니다.

### 4-4. 메인 README.md 작성 (협업/평가용)
최상위 폴더에 있는 `README.md` 문서를 매주 업데이트하여 학위/과제 포트폴리오를 구성합니다.
- **프로젝트 개요**: 본인의 이름 / 학번 / 생물자원가공공학 과제 레포지토리임을 명시
- **주차별 업데이트 내역**: 
  - `[Week 02]` 사과 윤곽선 인식 및 원형도/구형도 산출 스크립트 개발 완료
  - `[Week 03]` (차주 진행 시 업데이트)

---
*과제 제출 완료 후, 본인의 GitHub 저장소 URL(예: `https://github.com/아이디/biomaterial-handling/tree/main/week02`)을 조교/교수에게 제출하여 최종 성적에 반영합니다.*
