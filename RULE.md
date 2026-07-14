# LocalHub 개발 규칙 (RULE.md)

> 이 문서는 Frontend AI와 Backend AI가 **매번 작업을 시작하기 전에 반드시 읽고 따라야 하는 규칙**입니다.
> API 스펙, 데이터 모델, 협업 규칙을 정의합니다. 이 문서에 없는 기능은 구현하지 않습니다 (Won't have 참고).

---

## 0. 프로젝트 개요

| 항목        | 내용                                            |
| ----------- | ----------------------------------------------- |
| 서비스명    | LocalHub                                        |
| 대상 권역   | 서울 (핫플레이스 다건 지원, 예: 성수동/홍대 등) |
| 타깃 사용자 | 인증 없는 익명 사용자                           |
| Frontend    | Vue.js 3, 배포: Netlify                         |
| Backend     | FastAPI + SQLite, 배포: Render                  |
| 인증 체계   | **없음** (세션/로그인/회원가입 절대 구현 금지)  |

### 화면 구성 (와이어프레임 기준)

1. **메인 화면**: 서울 전역 지도(핫플레이스 핀 표시) + 우측 실시간 핫플 순위 위젯
2. **게시판 목록**: 특정 장소(Place)에 속한 게시글 목록
3. **게시글 상세**
4. **게시글 작성**
5. **AI 챗봇 플로팅 위젯**: 모든 화면에 공통 노출

---

## 1. 절대 하지 말아야 할 것 (Won't have)

AI가 임의로 아래 기능을 추가하는 것을 금지합니다. 요구사항에 없어도 "편의상" 구현하지 마세요.

- ❌ 스레드형 게시판 (대댓글, 댓글 자체도 미포함)
- ❌ 좋아요 기반 랭킹 (핫플 순위는 오직 게시글 개수로만 산정)
- ❌ 세션 ID, 로그인, 회원가입, JWT 등 인증/인가 체계
- ❌ 서울 외 타 권역 데이터, 정의되지 않은 부가 기능
- ❌ 프론트엔드에서 OpenAI API 직접 호출 (반드시 백엔드 프록시 경유)

---

## 2. 라벨링 규칙 (FE/BE 작업 추적)

모든 기능은 `FE-xx` (프론트엔드) 또는 `BE-xx` (백엔드) 라벨을 가집니다.

- AI는 작업을 시작하기 전 **9번 섹션의 체크리스트**를 확인하여 이미 완료된 라벨과 남은 라벨을 파악합니다.
- 기능 구현을 완료하면 반드시 9번 섹션의 해당 체크박스를 `[x]`로 갱신합니다.
- 커밋 메시지에 관련 라벨을 명시합니다. 예: `[BE-04] 게시글 작성 API 구현`
- 하나의 라벨은 하나의 독립적인 기능 단위입니다. 라벨 간 의존관계는 3번 섹션의 매핑표를 따릅니다.

---

## 3. 데이터 모델

### SigunguCode (시/군/구 지역코드 마스터) — 시드 데이터, 관리자 CRUD 없음

공공데이터 연동(유동인구/혼잡도 등)을 위해 장소를 법정동 시군구코드와 매핑하는 마스터 테이블입니다.

| 필드         | 타입        | 설명                                                             |
| ------------ | ----------- | ---------------------------------------------------------------- |
| sigungu_code | string (PK) | 시군구 코드 (공공데이터 원본 필드명: `lDongSignguCd`, 예: "350") |
| sido_name    | string      | 시/도명 (예: "서울특별시")                                       |
| sigungu_name | string      | 시/군/구명 (예: "성동구")                                        |

- 이 테이블은 애플리케이션에서 CRUD API로 노출하지 않고, 시드 데이터로만 관리합니다.
- 신규 장소(Place) 추가 시 반드시 이 마스터 테이블에 존재하는 `sigungu_code`를 참조해야 합니다.

### Place (장소/핫플레이스) — 시드 데이터, 관리자 CRUD 없음

| 필드         | 타입                                   | 설명                                                              |
| ------------ | -------------------------------------- | ----------------------------------------------------------------- |
| id           | int (PK)                               | 장소 ID                                                           |
| name         | string                                 | 장소명 (예: "성수동")                                             |
| lat          | float                                  | 위도                                                              |
| lng          | float                                  | 경도                                                              |
| description  | string \| null                         | 장소 설명                                                         |
| sigungu_code | string (FK → SigunguCode.sigungu_code) | 소속 시군구 코드 (공공데이터 매핑용, 원본 필드명 `lDongSignguCd`) |

### Post (게시글)

| 필드       | 타입                | 설명                                                  |
| ---------- | ------------------- | ----------------------------------------------------- |
| id         | int (PK)            | 게시글 ID                                             |
| place_id   | int (FK → Place.id) | 소속 장소                                             |
| nickname   | string              | 작성자 닉네임 (자유 입력, 미입력시 "익명")            |
| password   | string              | **4자리 숫자**, DB에는 해시로만 저장 (평문 저장 금지) |
| title      | string              | 제목                                                  |
| content    | string              | 본문                                                  |
| created_at | datetime            | 작성 시각                                             |

- 댓글 테이블은 만들지 않습니다.
- 비밀번호는 반드시 해시(bcrypt 등)로 저장합니다. API 응답에 password/password_hash 필드를 절대 포함하지 않습니다.

---

## 4. 공통 API 규칙

- 모든 API 경로는 `/api` 로 시작합니다.
- **JSON 필드명은 snake_case로 통일** (예: `place_id`, `created_at`). 프론트는 변환 없이 그대로 사용합니다.
- 성공 응답은 리소스(객체 또는 배열)를 감싸지 않고 그대로 반환합니다. (envelope 없음)
- 에러 응답은 FastAPI 기본 포맷을 따릅니다: `{"detail": "에러 메시지"}`
  - 404: 리소스 없음 / 400: 잘못된 요청(유효성 실패) / 403: 비밀번호 불일치
- 목록 조회는 페이지네이션을 지원합니다: 쿼리 파라미터 `page`(기본 1), `size`(기본 20)
  - 응답: `{"items": [...], "total": int, "page": int, "size": int}`
- CORS: 백엔드는 Netlify 배포 도메인 + `http://localhost:5173`(Vite 개발 서버)을 허용 origin으로 설정합니다.

---

## 5. API 명세

### 5.1 장소 / 지도 / 랭킹

**`BE-01` `GET /api/places`**
장소 목록 조회. 지도 핀 렌더링과 실시간 핫플 순위에 공용으로 사용됩니다.

- 응답은 `post_count`(해당 장소 게시글 총 개수) 기준 **내림차순 정렬**되어 반환됩니다. 프론트는 상위 N개를 잘라서 랭킹 위젯에 사용하면 됩니다.
- `sigungu_code`는 공공데이터 원본 필드명 `lDongSignguCd`를 snake_case로 변환한 값입니다 (SigunguCode 마스터 테이블 참조).
- Response 200:

```json
[
  {
    "id": 1,
    "name": "성수동",
    "lat": 37.5445,
    "lng": 127.0559,
    "description": "성수동 팝업/카페 거리",
    "sigungu_code": "350",
    "post_count": 12
  }
]
```

**`BE-02` `GET /api/places/{place_id}`**
장소 단건 조회 (post_count 포함, 응답 형식은 위 배열의 원소 1개와 동일).

- 404: 존재하지 않는 place_id

---

### 5.2 게시판 (장소별)

**`BE-03` `GET /api/places/{place_id}/posts`**
특정 장소의 게시글 목록 (페이지네이션). 목록 응답의 각 항목은 `content` 제외(목록에서는 title/nickname/created_at만).

- Query: `page`, `size`
- Response 200:

```json
{
  "items": [
    {
      "id": 10,
      "place_id": 1,
      "nickname": "익명",
      "title": "포켓몬 행사중",
      "created_at": "2026-07-14T10:00:00"
    }
  ],
  "total": 12,
  "page": 1,
  "size": 20
}
```

**`BE-04` `GET /api/places/{place_id}/posts/{post_id}`**
게시글 상세 조회 (content 포함, password 필드 제외).

- 404: 존재하지 않는 post_id

**`BE-05` `POST /api/places/{place_id}/posts`**
게시글 작성.

- Request:

```json
{ "nickname": "익명", "password": "1234", "title": "제목", "content": "내용" }
```

- 검증: `password`는 정확히 4자리 숫자 문자열이어야 함 (400)
- Response 201: 작성된 게시글 상세 (BE-04와 동일 형식)

**`BE-06` `PUT /api/places/{place_id}/posts/{post_id}`**
게시글 수정. 비밀번호 검증 필요.

- Request: `{ "password": "1234", "title": "제목", "content": "내용" }`
- 403: 비밀번호 불일치 / 404: 게시글 없음

**`BE-07` `DELETE /api/places/{place_id}/posts/{post_id}`**
게시글 삭제. 비밀번호 검증 필요.

- Request: `{ "password": "1234" }`
- 204: 성공 / 403: 비밀번호 불일치

---

### 5.3 AI 챗봇

**`BE-08` `POST /api/chatbot/summary`**
게시판 동향 요약. 백엔드가 OpenAI API를 프록시로 호출합니다 (API 키는 백엔드 `.env`에만 존재, 프론트/클라이언트에 절대 노출 금지).

- Request:

```json
{ "place_id": null, "question": "지금 어디가 붐벼?" }
```

- `place_id`가 `null`이면 서울 전역 게시글을 대상으로 요약 (기본 케이스)
- `place_id`가 있으면 해당 장소 게시글만 대상으로 요약
- `question`은 선택 입력 (없으면 일반 동향 요약)
- Response 200:

```json
{
  "summary": "성수동에 포켓몬 행사 때문에 사람이 몰려있어요. 우회를 추천합니다."
}
```

- 시스템 프롬프트 원칙:
  - 실제 게시글 데이터에 근거해서만 답변 (근거 없는 내용 생성 금지)
  - 답변은 2~3문장 이내로 간결하게
  - 인파/이벤트/우회 추천 등 실용적 톤 유지
  - 대상 게시글이 0건이면 "아직 데이터가 부족하다"는 취지로 답변

---

## 6. Frontend 작업 라벨

| 라벨    | 화면/기능                                       | 연동 API         |
| ------- | ----------------------------------------------- | ---------------- |
| `FE-01` | 지도 화면 (핀 렌더링)                           | `BE-01`          |
| `FE-02` | 실시간 핫플 순위 위젯 (메인 우측)               | `BE-01`          |
| `FE-03` | 핫플 항목/핀 클릭 → 게시판 목록 라우팅          | `BE-01`          |
| `FE-04` | 게시판 목록 화면 (페이지네이션 포함)            | `BE-03`          |
| `FE-05` | 게시글 상세 화면                                | `BE-04`          |
| `FE-06` | 게시글 작성 화면/폼 (닉네임/비밀번호/제목/내용) | `BE-05`          |
| `FE-07` | 게시글 수정/삭제 (비밀번호 확인 모달)           | `BE-06`, `BE-07` |
| `FE-08` | 챗봇 플로팅 위젯 UI (전 화면 공통)              | `BE-08`          |

---

## 7. 환경변수

### Backend (`.env`, 절대 커밋 금지)

```
OPENAI_API_KEY=
DATABASE_URL=sqlite:///./localhub.db
FRONTEND_ORIGIN=http://localhost:5173
```

### Frontend (`.env`)

```
VITE_API_BASE_URL=http://localhost:8000
```

---

## 8. 폴더 구조 규칙

```
/frontend   → Vue.js 3 프로젝트 (Netlify 배포 대상)
/backend    → FastAPI + SQLite 프로젝트 (Render 배포 대상)
/design     → 와이어프레임 등 디자인 산출물
RULE.md     → 본 문서 (루트 고정, 이동 금지)
```

- 프론트/백엔드는 서로의 폴더 내부 코드를 직접 수정하지 않습니다. API 계약(본 문서 5번 섹션)을 통해서만 소통합니다.
- API 계약을 변경해야 하는 경우, 코드를 먼저 짜지 말고 이 RULE.md의 5번 섹션을 먼저 갱신한 뒤 구현합니다.

---

## 9. 구현 체크리스트

작업 시작 전 아래 표를 확인하고, 기능 완료 시 체크박스를 갱신하세요.

### Backend

- [x] `BE-01` GET /api/places
- [x] `BE-02` GET /api/places/{place_id}
- [x] `BE-03` GET /api/places/{place_id}/posts
- [x] `BE-04` GET /api/places/{place_id}/posts/{post_id}
- [x] `BE-05` POST /api/places/{place_id}/posts
- [x] `BE-06` PUT /api/places/{place_id}/posts/{post_id}
- [x] `BE-07` DELETE /api/places/{place_id}/posts/{post_id}
- [x] `BE-08` POST /api/chatbot/summary
- [x] SigunguCode 마스터 테이블 시드 데이터 삽입
- [x] Place 시드 데이터 삽입 (최소 3곳 이상, sigungu_code 매핑 포함)

### Frontend

- [ ] `FE-01` 지도 화면
- [ ] `FE-02` 실시간 핫플 순위 위젯
- [ ] `FE-03` 핫플 클릭 → 게시판 라우팅
- [ ] `FE-04` 게시판 목록
- [ ] `FE-05` 게시글 상세
- [ ] `FE-06` 게시글 작성
- [ ] `FE-07` 게시글 수정/삭제
- [ ] `FE-08` 챗봇 플로팅 위젯
