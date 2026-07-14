import os
import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import SigunguCode, Place, Post
from ..database import SessionLocal

# In-memory storage for Seoul region JSON data
seoul_regions_data = []

# Hardcoded legal Sigungu Code mapping dictionary for data cleaning/validation
SIGUNGU_MAPPING = {
    "350": "성동구",
    "440": "마포구",
    "680": "강남구",
    "560": "영등포구"
}

def load_regions_data():
    """
    Loads region JSON data from local storage into memory during FastAPI startup.
    """
    global seoul_regions_data
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "seoul_regions.json")
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                seoul_regions_data = json.load(f)
            print(f"[DataLoader] Successfully loaded {len(seoul_regions_data)} regions into memory.")
        else:
            print(f"[DataLoader] Warning: {file_path} not found.")
            seoul_regions_data = []
    except Exception as e:
        print(f"[DataLoader] Error loading regions data: {e}")
        seoul_regions_data = []

def seed_database(db: Session):
    """
    Seeds SigunguCode and Place master tables if they are empty.
    """
    # 1. Seed SigunguCode Table
    existing_codes_count = db.query(SigunguCode).count()
    if existing_codes_count == 0:
        print("[DataLoader] Seeding SigunguCode master table...")
        sigungu_seeds = [
            SigunguCode(sigungu_code="350", sido_name="서울특별시", sigungu_name="성동구"),
            SigunguCode(sigungu_code="440", sido_name="서울특별시", sigungu_name="마포구"),
            SigunguCode(sigungu_code="680", sido_name="서울특별시", sigungu_name="강남구"),
            SigunguCode(sigungu_code="560", sido_name="서울특별시", sigungu_name="영등포구")
        ]
        db.add_all(sigungu_seeds)
        db.commit()
        print("[DataLoader] SigunguCode master table seeded successfully.")
    
    # 2. Seed Place Table
    existing_places_count = db.query(Place).count()
    if existing_places_count == 0:
        print("[DataLoader] Seeding Place master table...")
        place_seeds = [
            Place(id=1, name="성수동", lat=37.5445, lng=127.0559, description="성수동 팝업/카페 거리", sigungu_code="350"),
            Place(id=2, name="홍대", lat=37.5565, lng=126.9239, description="홍대 예술과 버스킹의 거리", sigungu_code="440"),
            Place(id=3, name="강남", lat=37.4979, lng=127.0276, description="강남역 트렌디한 쇼핑과 맛집", sigungu_code="680"),
            Place(id=4, name="여의도", lat=37.5216, lng=126.9242, description="여의도 한강공원과 금융가", sigungu_code="560")
        ]
        db.add_all(place_seeds)
        db.commit()
        print("[DataLoader] Place master table seeded successfully.")

def get_places_with_post_count(db: Session):
    """
    Retrieves all places, joined with their post counts, sorted by post count descending.
    """
    results = db.query(
        Place,
        func.count(Post.id).label("post_count")
    ).outerjoin(Post, Place.id == Post.place_id).group_by(Place.id).order_by(func.count(Post.id).desc()).all()
    return results

def get_local_context_for_ai(db: Session = None) -> str:
    """
    BE-1 to BE-2 Bridge Interface function:
    Compresses loaded places, attractions, and active hot place rankings into a clean
    string format that the OpenAI Chatbot can easily parse.
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    
    try:
        # 1. Format memory loaded tourist attractions
        regions_str = []
        for region in seoul_regions_data:
            attractions_str = ", ".join(region.get("attractions", []))
            regions_str.append(f"- {region['name']} (설명: {region['description']}, 주요 명소: {attractions_str})")
        
        # 2. Format database post count ranking
        ranking_results = get_places_with_post_count(db)
        ranking_str = []
        for rank, (place, post_count) in enumerate(ranking_results, 1):
            ranking_str.append(f"{rank}위. {place.name} (게시글 수: {post_count}개)")
        
        context_str = "=== 서울 권역 핫플레이스 및 관광지 정보 ===\n"
        if regions_str:
            context_str += "\n".join(regions_str) + "\n\n"
        else:
            context_str += "등록된 지역 정보 없음\n\n"
            
        context_str += "=== 실시간 핫플 랭킹 (게시글 수 기준) ===\n"
        if ranking_str:
            context_str += "\n".join(ranking_str)
        else:
            context_str += "등록된 랭킹 데이터 없음"
            
        return context_str
    except Exception as e:
        return f"Error assembling local context: {str(e)}"
    finally:
        if close_db:
            db.close()
