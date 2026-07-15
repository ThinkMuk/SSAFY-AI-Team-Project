import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import engine, Base, SessionLocal
import models
from routers import posts, chat

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB 테이블 생성
    Base.metadata.create_all(bind=engine)

    # BE 1 시드 데이터 로더가 존재하면 자동 실행 (협업 포인트)
    try:
        from utils.data_loader import load_initial_seed_data
        db = SessionLocal()
        try:
            load_initial_seed_data(db)
        finally:
            db.close()
    except (ImportError, AttributeError):
        pass

    yield
    # 서버 종료 시 cleanup 로직 (필요시)


app = FastAPI(
    title="LocalHub API Server",
    description="공공데이터 기반 지역 정보 공유 커뮤니티 LocalHub 백엔드 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정 (FE 허용 origin)
origins = [
    "http://localhost:5173",
    os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Chatbot-Warning"],
)

# BE 2 담당 라우터 등록
app.include_router(posts.router)
app.include_router(chat.router)

# BE 1 담당 라우터 유연한 등록 (존재 시 자동 등록)
try:
    from routers import places
    app.include_router(places.router)
except ImportError:
    pass


@app.get("/")
def read_root():
    return {"message": "LocalHub API Server Running (FastAPI + SQLite)"}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
