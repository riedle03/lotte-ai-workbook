# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 프로젝트 개요

- **프로젝트**: 롯데관광개발 임직원 대상 생성형 AI 실무 강의 자료 제작
- **강의 형식**: 50분 × 4차시 (4시간, 하루 연속 진행) | **4차시 8 Phase**
- **수강 대상**: 임직원 107명 (사전 설문 기준)
- **주력 도구**: Gemini (gemini.google.com) 무료 버전
- **보조 도구**: Claude, Perplexity (숙련자 보너스용)
- **강사**: 이대형
- **수강생 접속 URL**: `trpd.me/lottetour`
- **GitHub 저장소**: `riedle03/lotte-ai-workbook` (branch: `master`)

## 강의 핵심 메시지

> **"내 콘텐츠·내 문서·외부 정보·내 지식을 AI로 만들고 정리하는 4단계를 거쳐,**
> **4차시 끝에 본인 업무에 바로 쓸 결과물 4개를 손에 들고 나가는 강의"**

| Phase | 내용 | 주력 도구 |
|---|---|---|
| Phase 1·2 | 프롬프트 기초 · 문서·카피 | ChatGPT |
| Phase 3·4·5·6 | 나만의 챗봇 · Gemini 특화 · 이미지·영상 · 이미지 합성 | Gemini |
| Phase 7 | 데이터·보고 | ChatGPT |
| Phase 8 | 정보통합 (내 자료 학습 + 웹 리서치) | NotebookLM + Perplexity |

---

## 워크북 기술 아키텍처

### 파일 구조

```
workbook.html          ← 단일 파일. CSS + JS + HTML 전부 포함. 빌드 없음.
더미데이터팩/
  01_상품기획_분기판매현황.csv
  02~07_*.csv
의상합성_모델.png       ← Phase 6 실습 이미지 (8개)
의상합성_의상.png
목업합성_*.png (3개)
배경합성_*.png (3개)
```

### 배포

빌드 단계 없음. `git push origin master` = 즉시 배포 (GitHub Pages).

```powershell
git add workbook.html
git commit -m "설명"
git push origin master
```

이미지·CSV 추가 시 루트 또는 `더미데이터팩/`에 파일을 놓고 함께 커밋.

### 레이아웃 구조

```
.site-header           ← 고정 상단 헤더 (검정 배경)
.layout-wrapper        ← flex row
  .tab-nav             ← 사이드바 (width: 170px, position: sticky, height: 100vh)
    .sidebar-toggle    ← 접기/펴기 버튼 (collapsed 시 44px)
    .tab-btn × 9       ← Phase 0~8 탭 버튼
  .content-wrapper
    .tab-panel × 9     ← id="panel-0" ~ "panel-8", display:none/block
```

사이드바는 `overflow-y: auto; overscroll-behavior: contain`으로 독립 스크롤. `zoom` 미사용 — body font-size로만 크기 조정.

### CSS 디자인 토큰 (변경 금지)

```css
--blue: #024ad8;        /* 강조, 한 슬라이드 최대 2개 */
--blue-light: #c9e0fc;  /* so-what 콜아웃 배경 */
--ink: #1a1a1a;         /* 헤더 배경, 강조 텍스트 */
--cloud: #f7f7f7;       /* 페이지 배경 */
--canvas: #ffffff;      /* 카드 배경 */
--fog: #e8e8e8;         /* 구분선 */
--graphite: #636363;    /* 보조 텍스트 */
--coral: #ff5050;       /* 경고·Before 강조 */
--green: #0fa336;       /* 완료·After 강조 */
--shadow: 0 2px 8px rgba(26,26,26,0.08);
--r-card: 16px;         /* 카드 radius */
--r-btn: 4px;           /* 버튼 radius */
```

### JS 핵심 함수

**탭 전환**
```js
switchTab(idx)  // .tab-btn, .tab-panel 모두 .active 토글
// ※ panel id가 아닌 DOM 순서(인덱스) 기준 — id 값은 표시용
```

**파일 다운로드** (fetch → blob → anchor.download)
```js
downloadFile(btn, url, filename)
// url: GitHub raw URL (인코딩된 한국어 경로)
// filename: 수강생에게 보이는 파일명 (예: '[이미지1] 남성 모델 사진.png')
```

**프롬프트 복사**
```js
copyPrompt(btn, id)  // id로 엘리먼트 찾아 innerText 클립보드 복사
```

**복사 버튼 자동 주입** (DOMContentLoaded)
```js
// 모든 .prompt-card에 복사 버튼 자동 삽입
document.addEventListener('DOMContentLoaded', () => { … })
```

**사이드바 접기**
```js
toggleSidebar()  // .tab-nav에 .collapsed 토글 (width 170px ↔ 44px)
```

### GitHub Raw URL 패턴

새 파일을 다운로드 버튼에 연결할 때:
```
https://raw.githubusercontent.com/riedle03/lotte-ai-workbook/master/[URL인코딩된_경로]
```

한국어 파일명은 반드시 URL 인코딩. 예: `의상합성_모델.png` → `%EC%9D%98%EC%83%81%ED%95%A9%EC%84%B1_%EB%AA%A8%EB%8D%B8.png`

### 파일명 특수문자 주의

`[`, `]`가 포함된 파일을 PowerShell로 복사할 때 glob 오류 발생. `Copy-Item` 대신 사용:
```powershell
[System.IO.File]::Copy($source, $dest, $true)
```

---

## 작업 원칙

### 톤·표현
- "오늘" 금지 → "이번 차시" 또는 "여기까지"로 통일
- 강의 톤: 실무 중심·구체 예시·솔직한 한계 명시
- 추상적·뻔한 표현 금지 ("환상적인", "꿈에 그리던" 같은 AI 생성 카피는 Before 사례로만)

### 도구
- ChatGPT는 **호명만** — 본 시연 미사용 (별도 심화 과정 안내)
- **무료 도구만** 사용 (유료 라이선스 불필요)

### 데이터·보안
- **실데이터 절대 입력 금지** — 모든 실습은 더미 데이터
- 보안 안내 3분산: 사전 메일 / 1차시 시작 1~2분 (삼성전자 사례) / 매 차시 시연 직전 10초

### 직군 균형
- 시연은 일본 패키지 기획자 시나리오 1개
- 실습은 **7개 직군 모두** 자기 시나리오로 진행

---

## 파일 가이드

| 파일 | 내용 | 참조 시점 |
|---|---|---|
| `workbook.html` | **배포 메인 파일** — 수강생 워크북 | HTML 수정 시 |
| `01_강의_전체_설계.md` | 4차시 구조·블록·도구 매핑 | 강의안 본문 제작 시 |
| `02_설문_분석_데이터.md` | 107명 응답·직군 분포·니즈 순위 | 직군별 차별화 작업 시 |
| `03_롯데관광_회신_및_업무.md` | 5/22 회신·7가지 실제 업무·검수 협조 | 시나리오·예시 제작 시 |
| `04_프롬프트_원본_3종.md` | 프롬프트 마스터·Tona·메일 마스터 원본 | 1·2차시 핵심 시연 제작 시 |
| `05_책_22개_항목_분류.md` | 책 목차 1차 분류 (직접/카드/안내/제외) | 추가 프롬프트 검토 시 |
| `06_다음_작업_TODO.md` | 작업 우선순위와 의존 관계 | 무엇부터 할지 결정 시 |
| `07_업무력초격차를 만드는 AI 프롬프트 실무 활용법.md` | 책 전체 OCR 추출본 (58페이지) | 책 내용 참조 시 |
| `더미데이터팩/*.csv` | 7개 직군별 더미 CSV (Phase 7 실습) | Phase 7 다운로드 테이블 수정 시 |

---

## 강사 작업 스타일

- 개요·마크다운 먼저 → 검토 → 최종본 순서
- 단계별 확인 선호 — 한 번에 큰 결과물 비선호
- 모든 항목에 구체 예시 필수 (추상 항목 거부)
- 강사가 직접 시연 가능한 수준만
