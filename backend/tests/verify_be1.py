import sys
import os
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# backend 폴더를 sys.path에 동적으로 추가
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

from main import app
from database import Base, get_db
import models
from utils.data_loader import load_initial_seed_data, get_local_context_for_ai

# 테스트용 인메모리 SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestBE1Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        # BE 1 시드 데이터 로더 검증 및 삽입
        db = TestingSessionLocal()
        load_initial_seed_data(db)
        
        # 랭킹 테스트를 위해 장소 1에 게시글 2개, 장소 2에 게시글 1개 추가
        post1 = models.Post(place_id=1, nickname="테스터", password="1234", title="글1", content="내용1")
        post2 = models.Post(place_id=1, nickname="테스터", password="1234", title="글2", content="내용2")
        post3 = models.Post(place_id=2, nickname="테스터", password="1234", title="글3", content="내용3")
        db.add_all([post1, post2, post3])
        db.commit()
        db.close()

    def test_01_seed_data_loader(self):
        """[BE 1] 시드 데이터 삽입 및 중복 로드 방지 검증"""
        db = TestingSessionLocal()
        sigungu_count = db.query(models.SigunguCode).count()
        place_count = db.query(models.Place).count()
        self.assertGreaterEqual(sigungu_count, 5)
        self.assertGreaterEqual(place_count, 5)
        
        # 중복 호출 시 에러 없음 검증
        load_initial_seed_data(db)
        self.assertEqual(db.query(models.SigunguCode).count(), sigungu_count)
        self.assertEqual(db.query(models.Place).count(), place_count)
        db.close()

    def test_02_get_places_ranking(self):
        """[BE-01] 장소 목록 조회 및 post_count 내림차순 정렬 검증"""
        res = client.get("/api/places")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 5)
        
        # 첫 번째 장소는 게시글 2개가 있는 id=1이어야 하고 post_count=2여야 함
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[0]["post_count"], 2)
        
        # 두 번째 장소는 게시글 1개가 있는 id=2이어야 하고 post_count=1이어야 함
        self.assertEqual(data[1]["id"], 2)
        self.assertEqual(data[1]["post_count"], 1)
        
        # 내림차순 검증
        counts = [item["post_count"] for item in data]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_03_get_place_detail(self):
        """[BE-02] 장소 단건 조회 및 존재하지 않는 장소 404 검증"""
        res = client.get("/api/places/1")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["post_count"], 2)
        self.assertIn("sigungu_code", data)
        
        # 404 검증
        res_404 = client.get("/api/places/9999")
        self.assertEqual(res_404.status_code, 404)

    def test_04_get_local_context_for_ai(self):
        """[BE 1 인터페이스] get_local_context_for_ai 함수 동작 검증"""
        db = TestingSessionLocal()
        context_all = get_local_context_for_ai(None, db=db)
        self.assertIn("서울 전역 핫플레이스 실시간 랭킹", context_all)
        self.assertIn("종로구 (게시글 2건)", context_all)
        
        context_place = get_local_context_for_ai(1, db=db)
        self.assertIn("[장소 정보]", context_place)
        self.assertIn("이름: 종로구", context_place)
        self.assertIn("게시글 수: 2건", context_place)
        self.assertIn("글1", context_place)
        db.close()


if __name__ == "__main__":
    unittest.main()
