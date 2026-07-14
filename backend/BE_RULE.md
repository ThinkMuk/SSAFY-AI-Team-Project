# 🚀 LocalHub 백엔드 역할 분배 명세서 (BACK_ROLE.md)

> **프로젝트**: 공공데이터 기반 지역 정보 공유 커뮤니티 (LocalHub)
> **기간**: 3일 (타임어택)
> **기술 스택**: FastAPI, SQLite, SQLAlchemy, OpenAI API
> **협업 전략**: 파일 단위 물리적 격리를 통한 깃(Git) 충돌 방지 및 바이브 코딩(AI 코드 생성) 효율 극대화

---

## 🎯 기본 개발 원칙 (For Human & AI)
1. **도메인 분리**: BE 1은 정적 데이터(JSON)와 랭킹 조회 위주, BE 2는 동적 데이터(DB CRUD)와 AI 외부 연동 위주로 개발한다.
2. **라우터 격리**: 각자의 담당 라우터 파일(`routers/map.py`, `routers/board.py` 등) 안에서만 코드를 작성하며, 타인의 도메인 파일을 직접 수정하지 않는다.
3. **CORS & 배포**: 인프라 충돌을 막기 위해 환경 세팅 및 서버 배포는 BE 2가 전담한다.

---

## 🧑‍💻 BE 1: 데이터, 맵, 랭킹 담당 (Data & Map Master)
공공데이터 JSON을 파싱하여 지도 데이터를 제공하고, DB를 조회하여 게시글 수 기반의 핫플 랭킹을 산정하는 역할입니다.

* **주요 작업 파일**: `main.py` (Lifespan 부분), `utils/data_loader.py`, `routers/map.py`, `routers/ranking.py`
* **세부 담당 업무**:
  * **[데이터 로드]** FastAPI Lifespan 이벤트를 활용하여 서버 구동 시 권역 JSON 데이터를 메모리에 로드
  * **[마스터 데이터]** 법정동 시군구 코드 매핑 딕셔너리 하드코딩 및 데이터 정제
  * **[지도 API]** 프론트엔드 지도 핀 시각화를 위한 좌표/관광지 정보 반환 API 구현 (`GET /api/map/places`)
  * **[랭킹 API]** SQLite DB를 조회하여 게시판의 게시글 수 총합을 기준으로 한 실시간 핫플 랭킹 반환 API 구현 (`GET /api/board/ranking`)

---

## 🤖 BE 2: 코어, AI, 인프라 담당 (Core & AI Wizard)
커뮤니티의 핵심인 게시판 DB 통신을 처리하고, OpenAI를 연동해 챗봇에 생명력을 불어넣으며 서버 환경을 책임지는 역할입니다.

* **주요 작업 파일**: `database.py`, `models.py`, `routers/board.py`, `routers/chat.py`, `main.py` (CORS 세팅)
* **세부 담당 업무**:
  * **[인프라]** CORS 설정, `.env` 환경 변수 관리, Render 서버 배포 세팅 전담
  * **[코어 DB]** SQLite DB 및 SQLAlchemy ORM 스키마 설계 (게시글 테이블)
  * **[게시판 CRUD]** 익명 게시판 API 5종 및 페이지네이션 구현 (`GET`, `POST`, `PUT`, `DELETE /api/board`)
  * **[보안]** 게시글 `PUT/DELETE` 시, 평문 비밀번호 검증을 통한 권한 방어 로직 구현
  * **[AI 챗봇]** `POST /api/chat` 엔드포인트 구현 및 게시판 동향(인파, 이슈 등)을 포함한 요약 응답 프롬프트 엔지니어링

---

## 🤝 인터페이스 약속 (Cross-Domain 연동 포인트)
AI 챗봇(BE 2)이 지역 관광지 정보나 랭킹을 기반으로 대답해야 하므로, 아래의 함수 1개를 BE 1이 생성하여 BE 2에게 제공합니다.

* **요청 함수명**: `get_local_context_for_ai()`
* **구현자**: BE 1
* **사용자**: BE 2 (챗봇 프롬프트에 주입)
* **목적**: 현재 메모리에 로드된 특정 구역의 관광지 리스트와 핫플 랭킹 결과를 단순한 '문자열(String)' 형태로 압축하여 반환. (AI가 읽기 편한 포맷으로 가공)

---

## 🛑 AI 프롬프트 가이드 (System Instruction)
이 문서를 읽고 있는 AI Assistant는 코드를 생성할 때 다음 규칙을 절대적으로 준수할 것:
1. 사용자가 BE 1 역할을 수행 중일 때, `database.py`의 구조를 임의로 변경하거나 `routers/board.py`를 수정하는 코드를 제안하지 마시오. 랭킹 API는 오직 데이터 '조회(SELECT)'에만 집중하시오.
2. 사용자가 BE 2 역할을 수행 중일 때, JSON 파싱 로직을 직접 구현하지 말고 BE 1이 작성해 둔 유틸리티 함수를 `import` 하여 사용하도록 안내하시오.
3. FastAPI 라우터 코드를 생성할 때는 반드시 `APIRouter()`를 사용한 모듈화된 형태를 유지하시오.