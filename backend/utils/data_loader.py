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
        _load_export_block_posts(db, hashed_pw, rand_mins)


def _load_export_block_posts(db, hashed_pw, rand_mins):
    """ExportBlock 폴더의 노션 내보내기 사람이 직접 작성한 구별 실시간 글(사진 포함)을 적재합니다."""
    import os
    import glob
    import base64
    from datetime import datetime

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    export_defs = [
        # 1. 강남구 (place_id: 23)
        ("강남구", 23, "싸피출근고수", "강남역에서 사고나서 버스 다 서있어요..",
         "### 🚨 강남역 인근 광역버스 정렬 및 대기 지연 안내\n\n아… 강남역에서 사고 났다.. 다들 그냥 걸어가라. 지금 30분째 강남역이야… 하.. 오늘 SSAFY 발표날인데 하..", "image.png"),
        # 2. 강동구 (place_id: 25)
        ("강동구", 25, "고구마말랭이", "오늘 강동구 버스 안 섭니다!!!",
         "### 🚧 암사동 선사문화축제 교통 통제 안내\n\n아 서울시동부교육원 오늘 버스 안 와요.. 무슨 축제 때문이라는데 하 택시 타고 갑니다.. 다들 저처럼 정류장 오지 마세요!", "image 1.png"),
        # 3. 강북구 (place_id: 9)
        ("강북구", 9, "평화로운수유역", "[초비상] !! 수유역 흉기 난동 !!",
         "### ⚠️ 수유역 인근 긴급 상황 주의 안내\n\n수유역 지금 칼 든 사람 있어요 오지 마세요!!!! 수유역 지금 칼 든 사람 있어요!!!!", "b1a5fbf9-7085-4b20-9606-a034ae72ce01.png"),
        # 4. 강서구 (place_id: 16)
        ("강서구", 16, "레이가제일조하", "강서구 차 댈 곳이 하나도 없어요 하나도요..",
         "### 🚗 김포공항 및 강서구 일대 주차 대란 현황\n\n지금 강서구 차 엄청 많습니다.. 차 끌고 오지 마세요.. 어떻게 알았냐고요..? 하… 알고 싶지 않았습니다.", "image 2.png"),
        # 5. 관악구 (place_id: 21)
        ("관악구", 21, "공중주파", "관악산 사람 왜 이렇게 많아..?",
         "### ⛰️ 주말 관악산 등산객 밀집 현황\n\n아니 뭐 방송에라도 나왔나요..?? 등산로 입구부터 사람이 가득 찼습니다. 미친 거 아닌가요 진짜", "image 3.png"),
        # 6. 광진구 (place_id: 5)
        ("광진구", 5, "사자보이즈사랑해", "뚝섬한강공원에 케대헌이 떴다!!! 와",
         "### ✨ 뚝섬한강공원 드론 라이트쇼 & 피크닉 현장\n\n레전드.. 그런데 화장실 줄 엄청 길어서.. 오줌은 좀 참고 봐야 해요.. 드론쇼 명당 자리 공유합니다!", "image 4.png"),
        # 7. 구로구 (place_id: 17)
        ("구로구", 17, "미친사람", "신도림 환승구간 미쳤냐고 퇴근길 진짜",
         "### 🚉 신도림역 1호선-2호선 퇴근길 환승 혼잡\n\n신도림 환승구간 미친 거냐고 진짜 이걸 어떻게 가!!!!!!!!!! 에스컬레이터 탑승까지 20분 넘게 걸립니다.", "image 5.png"),
        # 8. 금천구 (place_id: 18)
        ("금천구", 18, "집돌이", "가산 디지털단지 수출의 다리 다들 아시죠..?",
         "### 🚙 가산 IT단지 수출의 다리 극심한 차량 정체\n\n이리로 오면 그냥 오늘 차에서 자는 거에요 오지 마세요. 퇴근 시간대 병목 현상 역대급입니다.", "image 6.png"),
        # 9. 노원구 (place_id: 11)
        ("노원구", 11, "닭돌이", "미쳤다 미쳤다 닭강정 맛집 노원 상륙",
         "### 🍗 노원역 신규 오픈 닭강정 맛집 대기열 안내\n\n지금은 사람 너무 많아서 내일 한번 가봐야겠다. 와 닭강정 죽었다 진짜!! 포장 대기만 100팀 넘어요.", "image 7.png"),
        # 10. 도봉구 (place_id: 10)
        ("도봉구", 10, "도봉돌이", "도봉구역 사람 진짜 많아요..",
         "### 🚇 도봉산역 등산객 집중으로 인한 개찰구 혼잡\n\n뭐지 주말인데 출근하는 기분..? 환승 통로랑 등산로 입구까지 발 디딜 틈이 없습니다.", "image 8.png"),
        # 11. 동대문구 (place_id: 6)
        ("동대문구", 6, "타코킬러", "와 경동시장에 가성비 타코 떴다",
         "### 🌮 경동시장 청년몰 가성비 타코 팝업스토어 후기\n\n광화문 가서 먹으면 인당 2만원 나오는 거 알죠..? 여긴 두당 2만원입니다 와우! 오픈 첫날부터 웨이팅 대박이네요.", "image 9.png"),
        # 12. 동작구 (place_id: 20)
        ("동작구", 20, "요가쌉고수", "미친 노들섬 무료 요가 클래스 열렸다 선셋요가클래스!!",
         "### 🧘 노들섬 잔디광장 선셋 요가 클래스 오픈\n\n와 지금 무료 신청이에요!! 전 신청 됐습니다 요가가 공짜!! 일몰 보면서 요가하는 분위기 진짜 최고입니다.", "image 10.png"),
        # 13. 마포구 (place_id: 14)
        ("마포구", 14, "불갈이", "망원에서 세계 불꽃 축제 열렸어요!!",
         "### 🎆 망원한강공원 서울세계불꽃축제 관람 실황\n\n미친.. 개이뻐요 다들 창밖 보세요!! 망원한강공원 쪽에서 보는 불꽃쇼 시야 확 트여서 장관입니다.", "image 11.png"),
        # 14. 서대문구 (place_id: 13)
        ("서대문구", 13, "신촌죽돌이", "뭐야 오늘 신촌 연세로에 차 왜 없어요..?",
         "### 🚶 신촌 연세로 차 없는 거리 행사 진행 안내\n\n차가 없는데요? 뭐지 오늘 차 없는 거리 행사 중이라 버스들 전부 우회 운행하고 있습니다. 정류장 위치 확인하세요!", "image 12.png"),
        # 15. 서초구 (place_id: 22)
        ("서초구", 22, "배고픈맷돼지", "오 오늘 반포 한강공원에서 야시장 열렸는데요?",
         "### 🌙 반포 한강공원 세빛섬 달빛 푸드트럭 야시장\n\n뭐냐? 푸드트럭 맛있네요? 3트럭째 클리어 중입니다. 큐브스테이크랑 야끼소바 꼭 드셔보세요!", "image 13.png"),
        # 16. 성동구 (place_id: 4)
        ("성동구", 4, "알런지", "성동구 오늘 오지 마세요 오지 마세요 포켓몬 팝업하는데 와",
         "### ⚡ 성수동 연무장길 포켓몬 플래그십 팝업 대기 현황\n\n아니 나도 알고 싶지 않았다구요,,, 오지 마요 진짜.. 인도까지 대기줄로 꽉 차서 이동조차 안 됩니다.", "image 14.png"),
        # 17. 성북구 (place_id: 8)
        ("성북구", 8, "주심조", "낙산공원에 소리지르는 사람 있어요",
         "### 🌃 한양도성길 낙산공원 야간 산책로 주의사항\n\n다들 조심하세요 ㅠㅠ 밤늦게 소리지르고 난동 부리는 사람이 있으니 심야 산책 시 일행과 함께 이동하시길 바랍니다.", "image 15.png"),
        # 18. 송파구 (place_id: 24)
        ("송파구", 24, "석천이", "석촌호수 벚꽃 이쁘게 폈습니다 ㅎㅎ",
         "### 🌸 석촌호수 벚꽃축제 개화 현황 및 산책 후기\n\n사람 좀 많긴 한데.. 올 만합니다..!! 동호와 서호 산책로 우측통행 준수해 주시면 쾌적하게 구경할 수 있어요.", "image 16.png"),
        # 19. 양천구 (place_id: 15)
        ("양천구", 15, "프로야근러", "아니 왜 밤 10시에 차가 더 막히냐고",
         "### 🚘 목동 학원가 하원 시간대 픽업 차량 병목 현황\n\n아 막힐까 봐 야근했는데 이거 억까 뭐냐.. 4시간 자겠네 하.. 밤 10시 정각 학원 앞 도로 완전히 마비입니다.", "image 17.png"),
        # 20. 영등포구 (place_id: 19)
        ("영등포구", 19, "드론쇼매니아", "여의도 한강공원에 드론쇼 해요!",
         "### 🚁 여의도 한강공원 1,000대 규모 눕방 드론 라이트쇼\n\n진짜 이뻐요 밖에 나오세요! 밤하늘을 수놓는 대규모 드론 라이트쇼가 여의도 잔디밭 상공에서 진행 중입니다.", "image 18.png")
    ]

    export_posts = []
    current_time = datetime.utcnow()
    for place_name, p_id, nick, title, body, img_name in export_defs:
        img_matches = glob.glob(os.path.join(base_dir, "ExportBlock*", img_name))
        content = body
        if img_matches and os.path.exists(img_matches[0]):
            try:
                with open(img_matches[0], "rb") as f:
                    b64_str = base64.b64encode(f.read()).decode("ascii")
                content += f"\n\n![{place_name} 실시간 사진](data:image/png;base64,{b64_str})"
            except Exception:
                pass
        
        export_posts.append(
            models.Post(
                place_id=p_id,
                nickname=nick,
                password=hashed_pw,
                title=title,
                content=content,
                created_at=current_time
            )
        )
    if export_posts:
        db.add_all(export_posts)
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
