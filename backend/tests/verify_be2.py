import sys
import os
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# backend 폴더를 sys.path에 동적으로 추가 (어떤 PC에서 실행하든 동작하도록)
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

from main import app
from database import Base, get_db
import models

# 테스트용 인메모리 SQLite DB (StaticPool로 모든 커넥션에서 동일 DB 공유)
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


class TestBE2Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        # 테스트 마스터 데이터 삽입 (SigunguCode, Place)
        db = TestingSessionLocal()
        sigungu = models.SigunguCode(sigungu_code="350", sido_name="서울특별시", sigungu_name="성동구")
        db.add(sigungu)
        place = models.Place(id=1, name="성수동", lat=37.5445, lng=127.0559, description="성수 팝업 거리", sigungu_code="350")
        db.add(place)
        db.commit()
        db.close()

    def test_01_create_post_success(self):
        """[BE-05] 게시글 작성 성공 검증 (4자리 비밀번호)"""
        res = client.post("/api/places/1/posts", json={
            "nickname": "테스터",
            "password": "1234",
            "title": "첫 게시글",
            "content": "성수동 팝업스토어 후기입니다."
        })
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["title"], "첫 게시글")
        self.assertEqual(data["nickname"], "테스터")
        self.assertNotIn("password", data)
        self.assertNotIn("password_hash", data)

    def test_02_create_post_invalid_password(self):
        """[BE-05] 4자리 숫자가 아닌 비밀번호 입력 시 400 에러 검증"""
        res1 = client.post("/api/places/1/posts", json={
            "nickname": "테스터",
            "password": "123",  # 3자리
            "title": "실패글",
            "content": "내용"
        })
        self.assertEqual(res1.status_code, 400)

        res2 = client.post("/api/places/1/posts", json={
            "nickname": "테스터",
            "password": "abcd",  # 문자
            "title": "실패글",
            "content": "내용"
        })
        self.assertEqual(res2.status_code, 400)

    def test_03_list_posts(self):
        """[BE-03] 장소별 게시글 목록 조회 및 content/password 제외 검증"""
        res = client.get("/api/places/1/posts")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("items", data)
        self.assertEqual(data["total"], 1)
        item = data["items"][0]
        self.assertNotIn("content", item)
        self.assertNotIn("password", item)

    def test_04_get_post_detail(self):
        """[BE-04] 게시글 상세 조회 검증"""
        res = client.get("/api/places/1/posts/1")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["content"], "성수동 팝업스토어 후기입니다.")
        self.assertNotIn("password", data)

    def test_05_update_post(self):
        """[BE-06] 게시글 수정 - 비밀번호 검증 (성공 200 / 실패 403)"""
        # 틀린 비밀번호 (403)
        res_fail = client.put("/api/places/1/posts/1", json={
            "password": "9999",
            "title": "수정된 제목",
            "content": "수정된 내용"
        })
        self.assertEqual(res_fail.status_code, 403)

        # 맞은 비밀번호 (200)
        res_ok = client.put("/api/places/1/posts/1", json={
            "password": "1234",
            "title": "수정된 제목",
            "content": "수정된 내용"
        })
        self.assertEqual(res_ok.status_code, 200)
        self.assertEqual(res_ok.json()["title"], "수정된 제목")

    def test_06_delete_post(self):
        """[BE-07] 게시글 삭제 - 비밀번호 검증 (성공 204 / 실패 403)"""
        # 틀린 비밀번호 (403)
        res_fail = client.request("DELETE", "/api/places/1/posts/1", json={"password": "9999"})
        self.assertEqual(res_fail.status_code, 403)

        # 맞은 비밀번호 (204)
        res_ok = client.request("DELETE", "/api/places/1/posts/1", json={"password": "1234"})
        self.assertEqual(res_ok.status_code, 204)

        # 삭제 후 조회 시 404
        res_get = client.get("/api/places/1/posts/1")
        self.assertEqual(res_get.status_code, 404)

    def test_07_chatbot_summary(self):
        """[BE-08] AI 챗봇 요약 API 호출 검증"""
        res = client.post("/api/chatbot/summary", json={
            "place_id": 1,
            "question": "지금 분위기 어때?"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("summary", data)

    def test_08_chatbot_smalltalk(self):
        """[BE-08] AI 챗봇 스몰톡/인사 질문 시 '데이터 없음' 거절 대신 친절한 안내 응답 검증"""
        res = client.post("/api/chatbot/summary", json={
            "place_id": 1,
            "question": "안녕? 너는 누구야?"
        })
        self.assertEqual(res.status_code, 200)
        summary = res.json()["summary"]
        self.assertIn("안녕하세요", summary)
        self.assertNotIn("데이터가 부족", summary)


if __name__ == "__main__":
    unittest.main()
