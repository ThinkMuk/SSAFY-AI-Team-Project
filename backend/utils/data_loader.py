from typing import Optional
from sqlalchemy.orm import Session
import models
from database import SessionLocal


def load_initial_seed_data(db: Session) -> None:
    """SigunguCode 및 Place 테이블에 초기 시드 데이터를 적재합니다."""
    # SigunguCode 시드 데이터 적재 (서울시 전체 25개 구)
    if db.query(models.SigunguCode).count() == 0:
        sigungu_seeds = [
            models.SigunguCode(sigungu_code="110", sido_name="서울특별시", sigungu_name="종로구"),
            models.SigunguCode(sigungu_code="140", sido_name="서울특별시", sigungu_name="중구"),
            models.SigunguCode(sigungu_code="170", sido_name="서울특별시", sigungu_name="용산구"),
            models.SigunguCode(sigungu_code="200", sido_name="서울특별시", sigungu_name="성동구"),
            models.SigunguCode(sigungu_code="215", sido_name="서울특별시", sigungu_name="광진구"),
            models.SigunguCode(sigungu_code="230", sido_name="서울특별시", sigungu_name="동대문구"),
            models.SigunguCode(sigungu_code="260", sido_name="서울특별시", sigungu_name="중랑구"),
            models.SigunguCode(sigungu_code="290", sido_name="서울특별시", sigungu_name="성북구"),
            models.SigunguCode(sigungu_code="305", sido_name="서울특별시", sigungu_name="강북구"),
            models.SigunguCode(sigungu_code="320", sido_name="서울특별시", sigungu_name="도봉구"),
            models.SigunguCode(sigungu_code="350", sido_name="서울특별시", sigungu_name="노원구"),
            models.SigunguCode(sigungu_code="380", sido_name="서울특별시", sigungu_name="은평구"),
            models.SigunguCode(sigungu_code="410", sido_name="서울특별시", sigungu_name="서대문구"),
            models.SigunguCode(sigungu_code="440", sido_name="서울특별시", sigungu_name="마포구"),
            models.SigunguCode(sigungu_code="470", sido_name="서울특별시", sigungu_name="양천구"),
            models.SigunguCode(sigungu_code="500", sido_name="서울특별시", sigungu_name="강서구"),
            models.SigunguCode(sigungu_code="530", sido_name="서울특별시", sigungu_name="구로구"),
            models.SigunguCode(sigungu_code="545", sido_name="서울특별시", sigungu_name="금천구"),
            models.SigunguCode(sigungu_code="560", sido_name="서울특별시", sigungu_name="영등포구"),
            models.SigunguCode(sigungu_code="590", sido_name="서울특별시", sigungu_name="동작구"),
            models.SigunguCode(sigungu_code="620", sido_name="서울특별시", sigungu_name="관악구"),
            models.SigunguCode(sigungu_code="650", sido_name="서울특별시", sigungu_name="서초구"),
            models.SigunguCode(sigungu_code="680", sido_name="서울특별시", sigungu_name="강남구"),
            models.SigunguCode(sigungu_code="710", sido_name="서울특별시", sigungu_name="송파구"),
            models.SigunguCode(sigungu_code="740", sido_name="서울특별시", sigungu_name="강동구"),
        ]
        db.add_all(sigungu_seeds)
        db.commit()

    # Place 시드 데이터 적재 (서울시 전체 25개 구 통일)
    if db.query(models.Place).count() == 0:
        place_seeds = [
            models.Place(id=1, name="종로구", lat=37.5730, lng=126.9794, description="서울특별시 종로구 지역 정보 공유", sigungu_code="110"),
            models.Place(id=2, name="중구", lat=37.5637, lng=126.9975, description="서울특별시 중구 지역 정보 공유", sigungu_code="140"),
            models.Place(id=3, name="용산구", lat=37.5326, lng=126.9900, description="서울특별시 용산구 지역 정보 공유", sigungu_code="170"),
            models.Place(id=4, name="성동구", lat=37.5633, lng=127.0371, description="서울특별시 성동구 지역 정보 공유", sigungu_code="200"),
            models.Place(id=5, name="광진구", lat=37.5385, lng=127.0823, description="서울특별시 광진구 지역 정보 공유", sigungu_code="215"),
            models.Place(id=6, name="동대문구", lat=37.5744, lng=127.0396, description="서울특별시 동대문구 지역 정보 공유", sigungu_code="230"),
            models.Place(id=7, name="중랑구", lat=37.6063, lng=127.0928, description="서울특별시 중랑구 지역 정보 공유", sigungu_code="260"),
            models.Place(id=8, name="성북구", lat=37.5894, lng=127.0167, description="서울특별시 성북구 지역 정보 공유", sigungu_code="290"),
            models.Place(id=9, name="강북구", lat=37.6398, lng=127.0255, description="서울특별시 강북구 지역 정보 공유", sigungu_code="305"),
            models.Place(id=10, name="도봉구", lat=37.6688, lng=127.0471, description="서울특별시 도봉구 지역 정보 공유", sigungu_code="320"),
            models.Place(id=11, name="노원구", lat=37.6542, lng=127.0568, description="서울특별시 노원구 지역 정보 공유", sigungu_code="350"),
            models.Place(id=12, name="은평구", lat=37.6027, lng=126.9291, description="서울특별시 은평구 지역 정보 공유", sigungu_code="380"),
            models.Place(id=13, name="서대문구", lat=37.5791, lng=126.9368, description="서울특별시 서대문구 지역 정보 공유", sigungu_code="410"),
            models.Place(id=14, name="마포구", lat=37.5663, lng=126.9016, description="서울특별시 마포구 지역 정보 공유", sigungu_code="440"),
            models.Place(id=15, name="양천구", lat=37.5170, lng=126.8665, description="서울특별시 양천구 지역 정보 공유", sigungu_code="470"),
            models.Place(id=16, name="강서구", lat=37.5509, lng=126.8495, description="서울특별시 강서구 지역 정보 공유", sigungu_code="500"),
            models.Place(id=17, name="구로구", lat=37.4954, lng=126.8874, description="서울특별시 구로구 지역 정보 공유", sigungu_code="530"),
            models.Place(id=18, name="금천구", lat=37.4569, lng=126.8955, description="서울특별시 금천구 지역 정보 공유", sigungu_code="545"),
            models.Place(id=19, name="영등포구", lat=37.5264, lng=126.8963, description="서울특별시 영등포구 지역 정보 공유", sigungu_code="560"),
            models.Place(id=20, name="동작구", lat=37.5124, lng=126.9393, description="서울특별시 동작구 지역 정보 공유", sigungu_code="590"),
            models.Place(id=21, name="관악구", lat=37.4782, lng=126.9515, description="서울특별시 관악구 지역 정보 공유", sigungu_code="620"),
            models.Place(id=22, name="서초구", lat=37.4836, lng=127.0327, description="서울특별시 서초구 지역 정보 공유", sigungu_code="650"),
            models.Place(id=23, name="강남구", lat=37.5172, lng=127.0473, description="서울특별시 강남구 지역 정보 공유", sigungu_code="680"),
            models.Place(id=24, name="송파구", lat=37.5145, lng=127.1059, description="서울특별시 송파구 지역 정보 공유", sigungu_code="710"),
            models.Place(id=25, name="강동구", lat=37.5301, lng=127.1238, description="서울특별시 강동구 지역 정보 공유", sigungu_code="740"),
        ]
        db.add_all(place_seeds)
        db.commit()

    # Post 시드 데이터 적재 (주요 핫플레이스 게시글 및 마크다운 샘플)
    if db.query(models.Post).count() == 0:
        import random
        from datetime import datetime, timedelta
        from routers.posts import get_password_hash
        hashed_pw = get_password_hash("8888")
        now = datetime.utcnow()

        def rand_mins(min_m, max_m):
            return now - timedelta(minutes=random.randint(min_m, max_m))

        post_seeds = [
            # 1위. 성동구 (place_id=4) - 글 5개 (성수동/서울숲 핫플)
            models.Post(
                place_id=4, nickname="성수탐험가", password=hashed_pw,
                title="성수동 감성 팝업스토어 대기 현황 (사진 포함)",
                content="### 성수동 디올 팝업 대기열 안내\n\n현재 메인 거리에 팝업 대기 인원이 꽤 많습니다. 방문 전 참고하세요!\n\n| 시간대 | 예상 대기시간 | 혼잡도 |\n|---|---|---|\n| 오후 1시 | 40분 | 보통 |\n| 오후 3시 | 90분 | **매우 혼잡** |\n\n- 주차장: 인근 공영주차장 만차\n- 추천 이동수단: 지하철 2호선 성수역\n\n![성수 거리](https://images.unsplash.com/photo-1517154421773-0529f29ea451?auto=format&fit=crop&w=600&q=80)",
                created_at=rand_mins(10, 25)  # 10~25분 전
            ),
            models.Post(
                place_id=4, nickname="서울숲주민", password=hashed_pw,
                title="서울숲 주차장 현재 만차입니다 대중교통 이용하세요",
                content="오늘 날씨가 좋아서 피크닉 온 분들이 정말 많네요.\n서울숲 공영주차장 진입로에서만 30분 넘게 기다려야 합니다.\n지하철 수인분당선 서울숲역 3번 출구로 나오시는 게 훨씬 빠릅니다!",
                created_at=rand_mins(40, 60)  # 40~60분 전
            ),
            models.Post(
                place_id=4, nickname="커피러버", password=hashed_pw,
                title="연무장길 카페 추천 베스트 3",
                content="1. **어니언 성수**: 빵 종류 다양하고 옥상 테라스 좋음\n2. **대림창고**: 층고 높고 넓어서 쾌적함\n3. **로우키**: 커피 맛이 정말 일품인 로스터리 카페\n\n> 주말 오후에는 세 곳 모두 웨이팅 필수입니다!",
                created_at=rand_mins(120, 180)  # 2~3시간 전
            ),
            models.Post(
                place_id=4, nickname="팝업러버", password=hashed_pw,
                title="성수 탬버린즈 플래그십 스토어 오픈 웨이팅",
                content="새로 오픈한 플래그십 스토어 현장 대기줄이 길게 서 있습니다.\n인증샷 찍기 좋은 조형물이 많으니 오후 4시 이후 한산할 때 방문하시는 것 추천해요.",
                created_at=rand_mins(300, 420)  # 5~7시간 전
            ),
            models.Post(
                place_id=4, nickname="빵순이", password=hashed_pw,
                title="뚝섬역 인근 베이커리 맛집 소금빵 출시 안내",
                content="뚝섬역 4번 출구 앞 베이커리에서 갓 구운 소금빵 나왔습니다.\n1인당 4개 구매 제한 있으니 참고하세요!",
                created_at=rand_mins(1440, 2000)  # 어제(1일 전)
            ),
            # 2위. 마포구 (place_id=14) - 글 4개 (홍대/연남 핫플)
            models.Post(
                place_id=14, nickname="홍대피플", password=hashed_pw,
                title="홍대 버스킹 실시간 현장 분위기 🔥",
                content="### 레드로드 버스킹존 현황\n\n금요일 저녁이라 댄스팀이랑 밴드 공연 벌써 시작했습니다.\n사람들이 둥글게 모여 있어서 통행은 조금 혼잡해요.\n\n![홍대 버스킹](https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=600&q=80)",
                created_at=rand_mins(15, 30)  # 15~30분 전
            ),
            models.Post(
                place_id=14, nickname="연트럴파커", password=hashed_pw,
                title="연남동 맛집 웨이팅 팁 및 추천 리스트",
                content="연트럴파크 쪽 맛집들은 **캐치테이블**이나 **테이블링** 원격 줄서기가 필수입니다.\n현장 대기 시 평균 1시간 이상 소요되니 출발 30분 전에 미리 앱으로 대기 거세요!",
                created_at=rand_mins(80, 110)  # 1~2시간 전
            ),
            models.Post(
                place_id=14, nickname="망원동주민", password=hashed_pw,
                title="망원시장 큐스닭강정 & 고로케 줄 현황",
                content="망원시장 유명 맛집들 줄이 꽤 길게 늘어서 있습니다.\n특히 고로케 집은 재료 소진으로 1시간 뒤 다시 구워진다고 합니다.",
                created_at=rand_mins(240, 360)  # 4~6시간 전
            ),
            models.Post(
                place_id=14, nickname="클러버", password=hashed_pw,
                title="홍대 클럽거리 주말 저녁 이동 동선 주의",
                content="주말 저녁 9시 이후 클럽거리 및 포차 거리에 유동인구가 집중되고 있습니다.\n차량 진입이 어려우니 도보나 대중교통 이용 바랍니다.",
                created_at=rand_mins(1500, 2200)  # 어제(1일 전)
            ),
            # 3위. 강남구 (place_id=23) - 글 3개 (강남역/신사 핫플)
            models.Post(
                place_id=23, nickname="강남직장인", password=hashed_pw,
                title="강남역 퇴근길 2호선 승강장 혼잡도 안내",
                content="### 2호선 퇴근길 실시간 혼잡도\n\n현재 오후 6시 30분 기준 개찰구부터 사람이 가득 찼습니다.\n가능하시면 신분당선이나 버스를 이용하시는 것을 추천합니다.\n\n- **강남역 -> 교대방면**: 극심한 혼잡\n- **강남역 -> 역삼방면**: 매우 혼잡",
                created_at=rand_mins(20, 45)  # 20~45분 전
            ),
            models.Post(
                place_id=23, nickname="가로수길산책", password=hashed_pw,
                title="신사동 가로수길 팝업 & 카페 동향",
                content="가로수길 메인 로드보다 골목 안쪽 세로수길에 예쁜 카페들이 더 많아졌어요.\n조용하게 대화하고 싶으신 분들은 안쪽 골목 추천합니다.",
                created_at=rand_mins(150, 210)  # 2~3시간 전
            ),
            models.Post(
                place_id=23, nickname="압구정로데오", password=hashed_pw,
                title="압구정 로데오 주말 핫플 분위기",
                content="저녁 7시 넘어가면서 라운지바랑 테라스 술집들 사람이 꽉 차기 시작했습니다.\n발렛 주차도 차가 몰려 출차까지 시간 걸리니 주의하세요.",
                created_at=rand_mins(1600, 2400)  # 1~2일 전
            ),
            # 4위. 종로구 (place_id=1) - 글 2개 (익선동/경복궁)
            models.Post(
                place_id=1, nickname="익선동나들이", password=hashed_pw,
                title="익선동 한옥거리 골목길 통행 안내",
                content="골목길이 좁은데 유동인구가 많아 우측 통행 부탁드립니다.\n인기 디저트 카페들은 2~3팀씩 웨이팅 있습니다.",
                created_at=rand_mins(30, 50)  # 30~50분 전
            ),
            models.Post(
                place_id=1, nickname="고궁탐방", password=hashed_pw,
                title="경복궁 야간개장 관람 후기 및 포토존 추천",
                content="### 경복궁 경회루 포토존\n\n밤에 물에 비친 경회루 모습이 정말 환상적입니다.\n삼각대 사용은 사람이 몰릴 때는 제한될 수 있으니 참고하세요!\n\n![경복궁 경회루](https://images.unsplash.com/photo-1548115184-bc6544d06a58?auto=format&fit=crop&w=600&q=80)",
                created_at=rand_mins(360, 480)  # 6~8시간 전
            ),
            # 5위. 용산구 (place_id=3) - 글 1개 (한남동/이태원)
            models.Post(
                place_id=3, nickname="한남동문화인", password=hashed_pw,
                title="한남동 리움미술관 인근 카페 동향",
                content="주말 전시 보고 나온 관람객들이 몰려서 한강진역 근처 카페 거의 다 만석입니다.\n이태원 쪽으로 조금 걸어 내려가시면 빈자리 찾기 쉽습니다.",
                created_at=rand_mins(60, 90)  # 1시간~1시간반 전
            ),
            # 6위. 송파구 (place_id=24) - 글 1개 (잠실/석촌호수)
            models.Post(
                place_id=24, nickname="잠실러닝맨", password=hashed_pw,
                title="석촌호수 산책로 주말 혼잡도 및 야경",
                content="### 롯데타워와 석촌호수 야경\n\n동호와 서호 산책로 모두 선선한 바람 불어서 걷기 좋습니다.\n러닝하시는 분들과 산책하시는 분들이 동선 겹치지 않게 주의 바랍니다.\n\n![석촌호수 야경](https://images.unsplash.com/photo-1616763355548-1b606f439f86?auto=format&fit=crop&w=600&q=80)",
                created_at=rand_mins(180, 240)  # 3~4시간 전
            ),
        ]
        db.add_all(post_seeds)
        db.commit()


def get_local_context_for_ai(place_id: Optional[int] = None, db: Optional[Session] = None) -> str:
    """AI 챗봇 프롬프트에 제공할 장소 및 랭킹 컨텍스트 문자열을 반환합니다."""
    close_db = False
    if db is None:
        from database import engine, Base
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        close_db = True
        try:
            if db.query(models.SigunguCode).count() == 0 or db.query(models.Place).count() == 0 or db.query(models.Post).count() == 0:
                load_initial_seed_data(db)
        except Exception:
            pass
    try:
        if place_id is not None:
            place = db.query(models.Place).filter(models.Place.id == place_id).first()
            if not place:
                return "존재하지 않는 장소입니다."
            
            post_cnt = db.query(models.Post).filter(models.Post.place_id == place_id).count()
            posts = db.query(models.Post).filter(models.Post.place_id == place_id).order_by(models.Post.created_at.desc(), models.Post.id.desc()).limit(10).all()
            post_texts = "\n".join([f"- {p.title}: {p.content[:50]}" for p in posts])
            
            return (
                f"[장소 정보]\n"
                f"이름: {place.name}\n"
                f"설명: {place.description or '설명 없음'}\n"
                f"게시글 수: {post_cnt}건\n"
                f"최신 게시글 요약/동향:\n{post_texts or '아직 등록된 게시글이 없습니다.'}"
            )
        else:
            places = db.query(models.Place).all()
            places_with_count = []
            for pl in places:
                cnt = db.query(models.Post).filter(models.Post.place_id == pl.id).count()
                places_with_count.append((pl, cnt))
            places_with_count.sort(key=lambda x: x[1], reverse=True)
            
            lines = []
            for pl, cnt in places_with_count[:10]:
                lines.append(f"- {pl.name} (게시글 {cnt}건): {pl.description or ''}")
            return "서울 전역 핫플레이스 실시간 랭킹 및 현황:\n" + "\n".join(lines)
    finally:
        if close_db:
            db.close()
