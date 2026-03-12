---
description: 한 주차 실습 자료 작성이 끝난 후 최종 배포(README 업데이트 및 Git Push)를 수행하는 워크플로우
---

# 주차별 실습 자료 최종 배포 워크플로우 (Publish Weekly Lab Workflow)

한 주차의 실습 자료(파이썬 스크립트, 마크다운 매뉴얼 등) 작성을 모두 마치고, 이를 GitHub에 최종 배포하기 위한 체크리스트이자 자동화 워크플로우입니다.

## 사용법 (Usage)
채팅에서 아래와 같이 입력:
```
/publish-week
```
또는
```
"N주차 자료 작성 다 끝났어. 배포 워크플로우 실행해줘."
```

## 워크플로우 단계 (Steps)

### 1. 국/영문 폴더 확인 (Sanity Check)
- 새로 작성된 `ko/weekN/` 및 `en/weekN/` 폴더 내에 누락된 스크립트나 이미지 파일이 없는지 점검합니다. 
- 영어 번역이 수행되지 않은 경우 먼저 `/translate-new-week` 를 수행해야 합니다.

### 2. README 문서 3종 동시 업데이트 (CRITICAL STEP)
가장 빈번하게 누락되는 과정입니다. 반드시 아래 3개의 `README.md` 파일에 새로운 주차 정보(N주차 주제, 설명, 사용 스크립트 목록 및 링크)를 추가합니다.

- **`README.md` (최상위 루트)**: 
  - 한국어 및 영어 테이블 양쪽에 N주차 항목 추가
  - **`📁 Repository Structure` 디렉터리 트리(`tree`)에 `weekN/` 폴더와 짧은 설명을 함께 추가**
- **`ko/README.md`**: `📂 주차별 실습 내용 요약` 에 `[Week N]` 제목과 상세 내용 추가
- **`en/README.md`**: `📂 Weekly Lab Summary` 에 `[Week N]` 제목과 상세 내용 추가

// turbo-all
### 3. 변경사항 스테이징 및 커밋 (Git Commit)
모든 생성 및 수정된 파일을 찾아 Git에 스테이징하고 커밋합니다.
```bash
git add .
git commit -m "Publish Week N Lab materials and update READMEs"
```

### 4. GitHub 저장소로 Push
```bash
git push origin main
```

### 5. 작업 완료 보고
- 커밋 아이디 및 푸시 성공 여부 확인
- 3종 README 모두 성공적으로 수정되었음을 유저에게 명시적으로 알림
