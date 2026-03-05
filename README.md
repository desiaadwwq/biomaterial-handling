# 🌾 생물자원가공공학 및 실습 (Biomaterial Handling & Processing)

본 저장소(Repository)는 **생물자원가공공학 및 실습** 교과의 주차별 프로그래밍 과제 및 데이터 분석 실습 코드를 통합 관리하기 위한 공식 포트폴리오(또는 제공용) 최상위 루트 공간입니다.

## 📌 저장소 목적 및 구성
본 과목에서는 수확 후 농산물 및 다양한 생물자원의 물리적, 광학적, 역학적 특성을 이해하고 이를 디지털 이미지 프로세싱(OpenCV) 등의 프로그래밍 기술을 활용하여 정량적으로 분석하는 실습을 진행합니다.

학생들은 매주 새롭게 제공되는 실습 주제별 **폴더(예: `week2`, `week3`...)** 내용물을 본인의 로컬 PC로 다운로드(Clone)하고 IDE에서 실습을 진행한 후, 각자의 GitHub 저장소에 변경/추가된 결과물을 `git add/commit/push` 하여 1학기 학습 이력을 누적해 나갑니다.

---

## 📂 주차별 실습 내용 요약

### [Week 01] 오리엔테이션 및 실습 기초 환경 구축
- 파이썬 및 GitHub 계정 세팅, 로컬 개발 환경(VS Code 등) 기초 설정 및 저장소 생성

### [Week 02] 기하학적 형태 지표(원형도, 구형도) 분석 알고리즘 구현
디지털 이미지 프로세싱 기초 기법들을 익히고, 영상을 활용해 사과 표본의 핵심 물리적 특성인 **원형도(Circularity)와 구형도(Sphericity)**를 산출합니다.
- **[A군] 정상 사과 데이터 ([`apple_side_A.png`](week2/apple_side_A.png), [`apple_top_A.png`](week2/apple_top_A.png))**: 둥글고 대칭에 가까운 정상 표본
- **[B군] 10% 왜곡 사과 데이터 ([`apple_side_B.png`](week2/apple_side_B.png), [`apple_top_B.png`](week2/apple_top_B.png))**: 한쪽 축이 일그러진 비대칭 표본
- **주요 학습 스크립트**:
  - [`step1_preprocess.py`](week2/step1_preprocess.py): 이미지 로딩 및 그레이스케일, 블러 노이즈 제거 전처리
  - [`step2_contour.py`](week2/step2_contour.py): Otsu 알고리즘 이진화 및 객체 윤곽선(Contour) 분리
  - [`step3_shape_analysis.py`](week2/step3_shape_analysis.py): 분리된 영상의 기하 특성(둘레, 면적) 추출 및 수식 기반 형태 지표(%, Circularity) 산출 및 시각화
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week2/02주차_원형도_구형도_실습_및_GitHub제출.md)**

### [Week 03] (이후 실습 내용 지속 업데이트 예정)
- (차주 업데이트...)

---

## 👩‍🏫 실습 구동 공통 안내
1. 항상 본 최상위 디렉터리(`works/` 도는 `biomaterial-handling/`) 전체를 IDE 프로그램에서 폴더 열기(Open Folder)로 열어주세요. 그래야 파이썬 터미널 실행 시 상대 경로 접근에 모순이 생기지 않습니다.
2. OpenCV, Numpy가 설치되지 않은 경우 터미널에서 다음 명령어로 설치합니다.
   ```bash
   pip install opencv-python numpy
   ```
3. 실습을 끝낸 후에는 반드시 이 `README.md` 문서를 스스로 수정 및 커밋하여, 본인이 어느 주차까지 마스터했는지 기록을 남기는 포트폴리오 용도로 활용하십시오.
4. 이해가 잘 되지 않을 때는 AI에게 문의를 해보기 바랍니다.

